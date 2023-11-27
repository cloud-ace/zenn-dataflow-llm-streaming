## 概要
Zenn記事「Dataflowを使った大規模言語モデル（LLM）のリアルタイム処理」のサンプルリポジトリ。

以下内容で構成されている。
- Apache Beamのmain.pyファイル
- Apache Beamのlocal実行用のlocal_main.pyファイル
- t5-baseモデルのstate_dict.pthファイルを作成するconvert_to_state_dict.pyファイル
- Pub/Subにメッセージを送信するpublish_texts.pyファイル

## 環境
- brew
- pipenv + pyenv
- python version: 3.11.4

## セットアップ

以下のコマンドで必要なライブラリをインストールします。
```
pip install -r requirements.txt
```

pipenvを使っている場合は以下のコマンドでセットアップできます。
```
pipenv sync
pipenv shell
```

以下を参考にして、git-lfsをインストールします。
https://github.com/git-lfs/git-lfs/wiki/Installation

例えば、Macの場合（brewを使っている場合）は以下のコマンドでインストールできます。
```
brew install git-lfs
```

## 実行準備
1. モデルのダウンロード
```
git clone https://huggingface.co/t5-base
```

2. state_dict.pthへの変換
```
mkdir t5-base-model
pipenv run python convert_to_state_dict.py
```


## 実行
### ローカル実行
```
python local_main.py --runner DirectRunner \
        --model_state_dict_path t5-base-model/state_dict.pth \
        --model_name t5-base
```

### DataflowRunner
Google Cloud 環境での実行方法を記載する。
事前に以下の必要なAPIに関しては有効化しておくこと。
- Dataflow API
- Cloud Pub/Sub API

1. プロジェクトIDを使って以下を実行する。
```
PROJECT_ID=<your project id> # GCPプロジェクトID
gcloud config set project $PROJECT_ID
```


2. GCSバケットを作成し、pthファイルをGCSにアップロードする
```
BUCKET=<your bucket name> # GCSバケット名
gcloud storage buckets create gs://$BUCKET
gcloud storage cp t5-base-model/state_dict.pth gs://$BUCKET/t5-base-model/state_dict.pth
```

3. Pub/Sub トピックの作成
```
TOPIC_NAME=<your topic name> # Pub/Subトピック名
gcloud pubsub topics create $TOPIC_NAME
```

4. 保存先のBigQueryデータセットの作成
```
DATASET_NAME=<your dataset name> # BigQueryデータセット名
bq --location=US mk --dataset $PROJECT_ID:$DATASET_NAME
```

5. Dataflowの実行
```
python main.py --runner DataflowRunner \
        --pubsub_topic projects/$PROJECT_ID/topics/$TOPIC_NAME \
        --model_state_dict_path gs://$BUCKET/t5-base-model/state_dict.pth \
        --model_name t5-base \
        --table_path $PROJECT_ID.$DATASET_NAME.dataflow_llm \
        --project $PROJECT_ID \
        --region us-central1 \
        --requirements_file requirements.txt \
        --staging_location gs://$BUCKET/staging \
        --temp_location gs://$BUCKET/tmp \
        --machine_type n1-highmem-16 \ \
        --disk_size_gb=200 \
        --streaming
```

UI上で起動が確認できたらCtrl+Cで上記コマンドは停止する。

6. Pub/Subにメッセージを送信する
```
python publish_texts.py --project_id $PROJECT_ID --topic $TOPIC_NAME
```

7. 処理を完了する場合は、UI上でDataflowジョブを停止する。


## 免責事項
このリポジトリに含まれる設定やソースコードはあくまでサンプルであり、動作保証やサポートは一切提供されません。
このリポジトリの使用によって生じるいかなる損害や問題についても、作者は一切の責任を負いません。使用者は自己の責任において利用してください。
実際のプロジェクトで使用する際には、適切にテストし、必要な変更を加えることを強くお勧めします。

## 参照
1. https://beam.apache.org/documentation/ml/large-language-modeling/
2. https://huggingface.co/t5-11b
3. https://qiita.com/masashi-ai/items/acbe9ba15017b848f19e
