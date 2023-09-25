

## 実行
1. モデルのダウンロード
git clone https://huggingface.co/t5-small

2. state_dict.pthへの変換
```
mkdir t5-small-model
pipenv run python convert_to_state_dict.py
```

### DirectRunner
```
pipenv run python main.py --runner DirectRunner \
                --model_state_dict_path t5-small-model/state_dict.pth \
                --model_name t5-small
```

### DataflowRunner
```
pipenv run python main.py --runner DataflowRunner \
                --model_state_dict_path <gs://path/to/saved/state_dict.pth> \
                --model_name t5-small \
                --project <PROJECT_ID> \
                --region us-central1 \
                --requirements_file requirements.txt \
                --staging_location <gs://path/to/staging/location> \
                --temp_location <gs://path/to/temp/location> \
                --experiments "use_runner_v2,no_use_multiple_sdk_containers" \
                --machine_type=n1-highmem-16 \
                --disk_size_gb=200
```


## 参照
1. https://beam.apache.org/documentation/ml/large-language-modeling/
2. https://huggingface.co/t5-11b
3. https://qiita.com/masashi-ai/items/acbe9ba15017b848f19e
