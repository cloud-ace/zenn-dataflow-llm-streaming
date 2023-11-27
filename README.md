## 概要
Zenn記事「Dataflowを使った大規模言語モデル（LLM）のリアルタイム処理」のサンプルリポジトリ。

以下内容で構成されている。
- Apache Beamのmain.pyファイル
- Apache Beamのlocal実行用のlocal_main.pyファイル
- t5-baseモデルのstate_dict.pthファイルを作成するconvert_to_state_dict.pyファイル
- Pub/Subにメッセージを送信するpublish_texts.pyファイル

## 環境
- brew
- python version: 3.11.4

## セットアップ

```
pipenv install
```


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
python main.py --runner DirectRunner \
        --model_state_dict_path t5-base-model/state_dict.pth \
        --model_name t5-base
```

### DataflowRunner
Google Cloud 環境での実行方法を記載する。
事前に以下の必要なAPIに関しては有効化しておくこと。
- Dataflow API
- Cloud Build API
- Cloud Pub/Sub API
- Cloud Storage API
- BigQuery API
- Artifact Registry API

1. 作成したpthファイルをGCSにアップロードする
```
gcloud storage cp t5-base-model/state_dict.pth gs://<BUCKET_NAME>/t5-base-model/state_dict.pth
```

1. Pub/Sub トピックの作成
```
gcloud pubsub topics create <TOPIC_NAME>
```

1. Dataflowの実行
```
python main.py --runner DataflowRunner \
        --pubsub_topic projects/ca-tasukuito-test/topics/llm-test \
        --model_state_dict_path gs://ca-tasukuito-test-llm/t5-base-model/state_dict.pth \
        --model_name t5-base \
        --table_path ca-tasukuito-test.bqml.dataflow_llm \
        --project ca-tasukuito-test \
        --region us-central1 \
        --requirements_file requirements.txt \
        --staging_location gs://ca-tasukuito-test-llm/staging \
        --temp_location gs://ca-tasukuito-test-llm/tmp \
        --machine_type n2-standard-64 \
        --streaming \
        --prebuild_sdk_container_engine cloud_build \
        --docker_registry_push_url us-central1-docker.pkg.dev/ca-tasukuito-test/dataflow-image \
        --sdk_location container
```


## 免責事項
このリポジトリに含まれる設定やソースコードはあくまでサンプルであり、動作保証やサポートは一切提供されません。
このリポジトリの使用によって生じるいかなる損害や問題についても、作者は一切の責任を負いません。使用者は自己の責任において利用してください。
実際のプロジェクトで使用する際には、適切にテストし、必要な変更を加えることを強くお勧めします。

## 参照
1. https://beam.apache.org/documentation/ml/large-language-modeling/
2. https://huggingface.co/t5-11b
3. https://qiita.com/masashi-ai/items/acbe9ba15017b848f19e
