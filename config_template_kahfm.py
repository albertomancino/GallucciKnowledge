TEMPLATE = """experiment:
  version: 0.3.1
  dataset: subdatasets_{sub}
  data_config:
    strategy: dataset
    dataset_path: {path}
    dataloader: KGFlexLoader
    side_information:
      work_directory: ../data/{dataset}
      map: ../data/{dataset}/mapping.tsv
      features: ../data/{dataset}/item_features.tsv
      predicates: ../data/{dataset}/predicate_mapping.tsv
  splitting:
    test_splitting:
      strategy: random_subsampling
      test_ratio: 0.2
      folds: 1
  top_k: 10
  evaluation:
    cutoffs: [10, 5, 1]
    simple_metrics: [nDCGRendle2020, HR, ItemCoverage, UserCoverage]
    relevance_threshold: 3
  gpu: 0
  external_models_path: ../external/models/__init__.py
  models:
    KaHFMEmbeddings:
      meta:
        hyper_max_evals: 10
        hyper_opt_alg: tpe
        validation_rate: 5
        verbose: True
        save_weights: False
        save_recs: True
        validation_metric: nDCGRendle2020@10
      epochs: 100
      batch_size: 512
      lr: [loguniform, -10, -1]
      l_w: [0.001, 0.003, 0.01]
      l_b: 0
       """
