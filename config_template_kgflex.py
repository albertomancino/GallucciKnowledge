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
      features: ../data/{dataset}/{sub}/new_item_features.tsv
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
    external.KGFlex:
      meta:
        verbose: True
        validation_rate: 5
        save_recs: True
        save_weights: False
        verbose: True
        validation_metric: nDCGRendle2020@10
      lr: 0.01
      epochs: 100
      q: 0.1
      embedding: [5, 10]
      parallel_ufm: 4
      first_order_limit: [200, 400]
      second_order_limit: [400]
      npr: [1, 2, 5]
      seed: 64
      criterion: infogain
      batch_size: 1024
      """
