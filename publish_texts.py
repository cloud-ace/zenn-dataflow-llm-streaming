from google.cloud import storage
from google.cloud import pubsub_v1
import time
import argparse

# Google Cloud Storageのバケット名とファイルのパス
bucket_name = "dataflow-samples"
# シェイクスピアのハムレットのテキスト
file_path = "shakespeare/hamlet.txt"


def publish_lines_to_pubsub(bucket_name, file_path, topic_name):
    storage_client = storage.Client()
    pubsub_publisher = pubsub_v1.PublisherClient()

    # ファイルを開いて1行ずつPub/Subにパブリッシュ
    with storage_client.bucket(bucket_name).blob(file_path).open("r") as file:
        for line in file:
            # 1行をPub/Subにパブリッシュ
            if line.lstrip().rstrip():
                pubsub_publisher.publish(topic_name, line.encode("utf-8"))
                print(f"published: {line}")
                time.sleep(5)


def get_args():
    """
    引数をparseするパーサ
    """
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--project_id",
        dest="pubsub_topic_project",
        required=True,
        help="Pub/Sub topic project id",
    )
    parser.add_argument(
        "--topic",
        dest="topic",
        required=True,
        help="Pub/Sub topic name",
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = get_args()
    publish_lines_to_pubsub(
        bucket_name,
        file_path,
        f"projects/{args.project_id}/topics/{args.topic}")
