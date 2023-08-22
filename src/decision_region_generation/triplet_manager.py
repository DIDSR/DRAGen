import sys
sys.path.append("../../")
from src.data_input import load_attributes, load_image
from itertools import product, combinations
import pandas as pd
import random
import math

class TripletManager():
    """ Wrapper class to generate vicinal distributions for specified groups.

    Parameters
    ----------
    input_csv : :obj:`str`
        File path for input csv; passed to :obj:`data_input.load_attributes`.
    classes : :obj:`dict`
        All potential output classes, organized by task.
    triplets_per_group : :obj:`int`
        Number of triplets to generate for each group of samples.
    subgroup_attributes : :obj:`dict`, `optional`
        All subgroup attributes options, organized by attribute; ex. {'Sex':['F','M']}
    image_rel_path : :obj:`str`, `optional`
        Relative image path; passed to :obj:`data_input.load_attributes`.
    sample_id_column : :obj:`str`, `optional`
        ID column for input csv; passed to :obj:`data_input.load_attributes`.
    mix_subgroups : :obj:`bool`, `optional`
        If true, will not separate groups by subgroup attributes.
    mix_classes : :obj:`bool`, `optional`
        If true, will not separate groups by class.
    """
    def __init__(self, input_csv, classes, triplets_per_group, subgroup_attributes=None, image_rel_path=None, sample_id_column=None, mix_subgroups=False, mix_classes=False, random_seed=None):
        self.input_csv = input_csv
        self.classes = classes
        self.triplets_per_group = triplets_per_group
        self.subgroup_attributes = subgroup_attributes
        self.mix_subgroups = mix_subgroups
        if self.subgroup_attributes is None:
            self.mix_subgroups = True
        self.mix_classes = mix_classes
        self.random_seed = random_seed
        print(f"random seed is {self.random_seed}")
        if self.random_seed is not None:
            random.seed(self.random_seed)
        self.sample_attributes = self._determine_attributes()
        self.df = load_attributes(self.input_csv, rel_path = image_rel_path, subgroup_information=self.sample_attributes, id_column=sample_id_column)
        self.groups = self._determine_groups()
        print(f"Created {len(self.groups)} groups:")
        for k, v in self.groups.items():
            print(f"\tgroup {k}: {v}")
        print(f"Generating {self.triplets_per_group*len(self.groups)} triplets ({self.triplets_per_group}/group)")
        self.triplets = self._generate_triplets()
        self.triplet_df = self._get_triplet_df()

    def _determine_attributes(self):
        """ Determine the separate attributes (if any) to not mix samples between """
        if self.mix_classes and self.mix_subgroups:
            return None
        elif self.mix_classes:
            return self.subgroup_attributes
        elif self.mix_subgroups:
            return self.classes
        else: 
            g = self.classes.copy()
            g.update(self.subgroup_attributes)
            return g

    def _determine_groups(self):
        """ Determine the unique sample groups to generate sample triplets from """
        groups = {}
        if self.sample_attributes is None:
            groups[0] = {}
        elif len(self.sample_attributes) == 1:
            for k in self.sample_attributes.keys():
                for i, v in enumerate(self.sample_attributes[k]):
                    groups[i] = {k:v}
        else:
            attribute_combinations = product(*list(self.sample_attributes.values()))
            for i, comb in enumerate(attribute_combinations):
                groups[i] = {}
                for ii, k in enumerate(self.sample_attributes.keys()):
                    groups[i][k] = comb[ii]
        # check that there are at least three patients in each group, if not, remove group
        id_col = "ID" if "ID" in self.df.columns else "Path"
        rm_groups = []
        for i, g in groups.items():
            temp_df = self.df.copy()
            for k,v in g.items():
                temp_df = temp_df[temp_df[k] == v]
            ids = temp_df[id_col].unique()
            if len(ids) < 3:
                # print(f"Fewer than 3 samples found for group {i} ({g}), skipping group...")
                rm_groups.append(g)
        groups = [g for g in groups.values() if g not in rm_groups]
        return {i:g for i,g in enumerate(groups)}

    def _generate_triplets(self):
        """ Generate triplets using sample IDs, or index if no ID is given"""
        id_col = "ID" if "ID" in self.df.columns else "Path"
        triplets = {}
        for i, g in self.groups.items():
            temp_df = self.df.copy()
            for k,v in g.items():
                temp_df = temp_df[temp_df[k] == v]
            ids = temp_df[id_col].unique()
            if len(ids) < 3:
                print(f"Fewer than 3 samples found for group {i} ({g}), skipping group...")
                continue
            all_triplets = tuple(combinations(ids, 3))
            # select random indices from all_triplets -> each ID should be used approximately the same number of times (TODO: check)
            n_potential_triplets = math.factorial(len(ids))/(math.factorial(3)*math.factorial(len(ids)-3))
            if n_potential_triplets < self.triplets_per_group:
                print(f"Cannot generate {self.triplets_per_group} triplets for group {i} ({g}), only {int(n_potential_triplets)} unique triplet(s) possible.")
                triplet_indices = [idx for idx in range(len(all_triplets))]
            else:
                triplet_indices = sorted(random.sample(range(len(all_triplets)), self.triplets_per_group))                
            triplets[i] = {ii:t for ii,t in enumerate(tuple(all_triplets[ti] for ti in triplet_indices))}
        return triplets

    def _get_triplet_df(self):
        """ Converts the triplet dictionary to a pandas.DataFrame """
        tdf = pd.DataFrame(columns=['group', 'triplet_number', 'triplet'])
        for g in self.triplets:
            for i, t in self.triplets[g].items():
                tdf.loc[len(tdf)] = [g,i,t]
        return tdf 

    def __getitem__(self, key):
        """ 
        Returns
        =======
        The triplet, group, key and images for the specified triplet: dict
        """
        id_col = "ID" if "ID" in self.df.columns else "Path"
        
        if type(key) == int:
            t = self.triplet_df.at[key, 'triplet']
            group = self.triplet_df.at[key, 'group']
        elif type(key) == tuple:
            t = self.triplet_df[(self.triplet_df['group'] == key[0]) & (self.triplet_df['triplet_number'] == key[1])]['triplet'].values[0]
            group = key[0]
            key = key[1]
        images = []
        for i in t:
            if id_col == 'Path':
                img_path = i
            else:
                img_path = self.df[self.df[id_col] == i]['Path'].sample(1).values[0]
            images.append(load_image(img_path))
        return {"triplet":t, 'group':group,'key':key, 'images':images}
    
    def __len__(self):
        return(len(self.triplet_df))

    def __iter__(self):
        for i in range(len(self)):
            yield self[i]
    
def random_combination(iterable, r):
    """ Random selection from itertools.combinations """      
    pool = tuple(iterable)
    n = len(pool)
    indices = sorted(random.sample(range(n),r))
    return tuple(pool[i] for i in indices)
