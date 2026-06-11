from sklearn.model_selection import GridSearchCV

class ModelTrainer:

    def __init__(self, model):

        self.model = model

    def tune(self, X, y):

        param_grid = {
            "model__n_estimators": [100, 200],
            "model__max_depth": [10, 20]
        }

        search = GridSearchCV(
            estimator=self.model.pipeline,
            param_grid=param_grid,
            cv=5,
            scoring="f1",
            n_jobs=1
        )

        search.fit(X, y)

        self.model.pipeline = search.best_estimator_

        return search