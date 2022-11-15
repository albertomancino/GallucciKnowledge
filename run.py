import config_template_kgflex
from elliot.run import run_experiment
import config_template_kahfm
import config_template_kahfm_features
import os
import argparse
import pandas as pd

templates = {'kahfm': config_template_kahfm.TEMPLATE,
             'kgflex': config_template_kgflex.TEMPLATE,
             'kahfm_features': config_template_kahfm_features.TEMPLATE}

config_dir = 'config_files/'
RANDOM_SEED = 42

parser = argparse.ArgumentParser()

parser.add_argument('--dataset', required=True, type=str, nargs='+')
parser.add_argument('--start', required=False, type=int, default=0)
parser.add_argument('--end', required=True, type=int)
parser.add_argument('--model', required=True, type=str)

args = parser.parse_args()

datasets = args.dataset
start = args.start
end = args.end
model: str = args.model.lower()

assert model in templates, f'model name not found. Accepted: {templates.keys()}'

template = templates[model]

print(f'Running from dataset n. {start} to n. {end}')

subdatasets = []
for dataset in datasets:
    for sub in range(start, end):
        subdataset = {'id': sub}
        path = f'./data/{dataset}/{sub}/dataset_filtered_ordered_g{sub}.tsv'
        path = os.path.abspath(path)
        assert os.path.exists(path), f'Missing dataset for {dataset} at sub {sub}'
        subdataset['path'] = path
        subdataset['dataset'] = dataset
        subdatasets.append(subdataset)

# run experiments on each generated dataset
for data in subdatasets:
    id_ = data['id']
    print(f'Running subdaset n.{id_}')
    df = pd.read_csv(data['path'], sep="\t", header=None)
    max_users = (df[0].nunique())*0.5
    max_items = (df[1].nunique())*0.5
    config = template.format(dataset=data['dataset'], sub=id_, path=data['path'], max_users=max_users, max_items=max_items)
    config_path = os.path.join(config_dir, 'runtime_conf.yml')
    with open(config_path, 'w') as file:
        file.write(config)
    run_experiment(config_path)
