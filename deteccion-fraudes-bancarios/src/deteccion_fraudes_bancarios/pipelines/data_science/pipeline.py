from kedro.pipeline import Node, Pipeline

from .nodes import evaluate_model, split_data, train_model, scale_data, train_clustering_model, evaluate_clustering_model, test_clustering_model


def create_pipeline(**kwargs) -> Pipeline:
    return Pipeline(
        [
            # Modelo Supervisado
            #Modelo de Clusterización
            Node(
                func=split_data,
                inputs=["data_preprocessed", "params:train_test_split"],
                outputs=["X_train", "X_test", "y_train", "y_test"],
                name="split_data_node"
            ),
            Node(
                func = scale_data,
                inputs=["X_train", "X_test"],
                outputs=["X_train_scaled", "X_test_scaled"],
                name="scale_data_node"
            ),
            Node(
                func=train_clustering_model,
                inputs=["X_train_scaled", "params:clustering_parameters"],
                outputs="clustering_model",
                name="train_clustering_model_node"
            ),
            Node(
                func=evaluate_clustering_model,
                inputs=["X_test_scaled", "clustering_model"],
                outputs=["cluster_labels", "clustering_metrics"],
                name="evaluate_clustering_model_node"
            ),
            Node(
                func=test_clustering_model,
                inputs=["X_test_scaled", "clustering_model", "params:umbral_anomalia"],
                outputs="cluster_labels_test",
                name="test_clustering_model_node"
            )
        ]
    )
