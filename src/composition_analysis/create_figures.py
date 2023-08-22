from matplotlib import rcParams, ticker, patches, cm, colors
from matplotlib.cm import ScalarMappable
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import h5py

def plot_figures(df, plot:str, save_loc:str, tasks:dict, palette:str|dict|list='Set2', aggregate:str='group', show_percent:bool=True,
                errorbar:bool=True, show:bool=False, save:bool=True, save_dpi:int=800, filepath:str=None, n_per_group:int=None,
                threshold:float=None, output_formats=['.svg']):
    """
    Plots composition, performance or region figures.

    Arguments
    =========
    df : pandas.DataFrame
        DataFrame containing decision region composition infromation; used with plot = composition or performance.
    plot
        Type of plot to create, options: composition, performance, region.
    save_loc
        Folder in which to save plot images.
    tasks
        Model classification tasks.
    palette
        Color palette to use. (TODO: expand description)
    aggregate
        Method by which to aggregate results, must match the aggregation used during composition analysis.
    show_percent
        If True, exact percent values will be included on composition/performance plots.
    errorbar
        If True, error bars will be included on composition/performance plots.
    show
        If True, will display plots.
    save
        If True, will save plot files to save_loc.
    save_dpi
        DPI of saved output image(s).
    filepath
        File path of decision region hdf5 file; only used for region figures.
    n_per_group
        Number of triplets per group to create plots for; only used for region figures.
    threshold
        The threshold to be applied to convert output scores to a binary classification, if None, no threshold is applied; only used for region figures.
    output_formats
        The image formats in which to save the output figures.
    """
    # process arguments
    plot_options = {'composition','performance', 'region'}
    aggregate_options = {'all','group','class', None}
    if plot not in plot_options:
        raise ValueError(f"aggregate must be in {plot_options}, not {plot}")
    if aggregate not in aggregate_options:
        raise ValueError(f"plot must be in {aggregate_options}, not {aggregate}")
    if aggregate == 'all' and plot == 'performance':
        raise ValueError("Cannot aggregate 'all' with plot = 'performance'")
    elif aggregate == 'all':
        df_info = {}
        for ii, row in df.iterrows():
            for c in df.columns:
                df_info[(c,ii)] = row[c]
        df = pd.DataFrame(df_info, index=['all'])
    if type(palette) == str:
        try:
            palette = cm.get_cmap(palette)
        except:
            raise ValueError(f"Unrecognized color map {palette}")
    if plot == 'region':
        fig = plot_decision_regions(filepath=filepath, save_loc=save_loc, n_per_group=n_per_group, threshold=threshold, palette=palette)
    else:
        width=0.5
        task = list(tasks.keys())[0]
        task_cols = [c.split(":")[-1] for c in set(df.columns.get_level_values(0)) if c.startswith(task) and ':' in c]
        if type(palette) == list:
            palette = {c:palette[i] for i,c in enumerate(task_cols)}
        elif type(palette) != dict:
            palette = {c:palette(i) for i,c in enumerate(task_cols)}
        if aggregate == 'group':
            df = df.reset_index().set_index('group')
        elif aggregate == 'class':
            df = df.reset_index().set_index(task)
        # set up figure
        pad = 1/( (len(df)+2)*1.5)
        if plot == 'composition':
            fig, ax = plt.subplots(figsize=(8, len(df)+2))
            plt.subplots_adjust(left=1/16, right=13/16, bottom=pad, top=1-pad)
            ax.set_title(task)
            ax.set_yticks(np.arange(len(df)), df.index)
            ax.set_ylim(-width, len(df)-width)
            ax.set_yticklabels([])
            ax.xaxis.set_minor_locator(ticker.AutoMinorLocator(2))
            # ax.xaxis.grid(True, which='minor')
            ax.set_xlim(0,100)
            ax.set_xlabel("Percent (%)")
            # Plot
            legend_elements = [patches.Patch(facecolor=palette[opt], label=opt) for opt in task_cols]
            fig.legend(handles=legend_elements, bbox_to_anchor=(13/16, pad, 3/16, 1-(pad*2)), mode='expand', loc='center') # TODO: Legend location
            for g, (label, row) in enumerate(df.iterrows()):
                if aggregate == 'class':
                    ax.text(50, g+(width/1.9), f"Triplet Class: {label}", ha='center', va='bottom')
                elif aggregate == 'group':
                    ax.text(50, g+(width/1.9), label, ha='center', va='bottom')
                base = 0
                for c in task_cols:
                    amount = row[f"{task}:{c}"]['mean']
                    err = row[f"{task}:{c}"]['std']
                    ax.barh(label, amount, width, label=c.split(":")[-1], left=base, color=palette[c.split(":")[-1]])
                    base += amount
                    if base < 100 and base > 0:
                        percent_text = f"{base:.2f}%"
                        if errorbar and not np.isnan(err):
                            ax.errorbar( amount, label, xerr=err, ecolor='black')
                            percent_text += f" (\u00B1{err:.2f}%)"
                        if show_percent:
                            if base < 5:
                                ha = 'left'
                            elif base > 95:
                                ha = 'right'
                            else: 
                                ha = 'center'
                            ax.text(base, g-(width/1.9), percent_text, ha=ha,va='top',fontsize=10)
                        
        elif plot == 'performance':
            fig, ax = plt.subplots(figsize=(len(df)+2,6))
            plt.subplots_adjust(left=pad, right=1-pad, bottom=1/9, top=8/9)
            ax.set_title(task)
            ax.set_ylim(0,100)
            ax.set_ylabel("Percent Correct (%)")
            ax.set_xlabel("Triplet Class")
            # Plot
            for i, (label, row) in enumerate(df.iterrows()):
                if aggregate == 'group':
                    amount = row[f"{task}:{row[task]['']}"]['mean']
                    err = row[f"{task}:{row[task]['']}"]['std']
                    c = palette[row[task]['']]
                elif aggregate == 'class':
                    amount = row[f"{task}:{label}"]['mean']
                    err = row[f"{task}:{label}"]['std']
                    c = palette[label]
                ax.bar(i, amount, width, color=c)
                if errorbar:
                    ax.errorbar(i, amount,yerr=err, ecolor='k')
                    if show_percent:
                        ax.text(i, amount,  f"{amount:.2f}%\n(\u00B1{err:.2f}%)", ha='left', va='bottom', fontsize=10)
                elif show_percent:
                    ax.text(i, amount,  f"{amount:.2f}%", ha='center', va='bottom', fontsize=10)
        
    if save:
        for out_format in output_formats:
            if not out_format.startswith('.'):
                out_format = '.' + out_format
            if plot == 'region':
                save_name = f"{save_loc}/decision_region_{plot}{out_format}"
            else:
                save_name = f"{save_loc}/decision_region_{plot}_{aggregate}{out_format}"
            plt.savefig(save_name, dpi=save_dpi)
            print(f"Plot saved at {save_name}")
    if show:
        plt.show()
    else:
        plt.close('all')

def plot_decision_regions(filepath:str, save_loc:str, n_per_group:int=None, threshold:int=1, palette:str='Set2'):
    """ Plot decision regions from decision region files.

    Notes
    =====
    TODO: 
    - threshold support: legend + palette
    
    Arguments
    =========
    filepath
        File path to decision region hdf5 file.
    save_loc
        Save location.
    n_per_group
        Number per group to plot; if `None`, plots all.
    threshold
        Ouput score threshold; if `None`, does not threshold
    
    Returns
    =======
    matplotlib.pyplot.figure
        Plot figure.
    """
    file = h5py.File(filepath, 'r')
    if threshold is None:
        norm = plt.Normalize(0,1)
    else:
        bounds = [0, threshold, 1]
        norm = colors.BoundaryNorm(bounds, palette.N)
    if type(palette) in {dict, list}:
        raise ValueError("A matplotlib colormap name must be  used when plotting 'region'.")
    if type(palette) == str:
        palette = plt.get_cmap(palette) 
    fig, axes = plt.subplots(len(file.keys()), n_per_group, squeeze=False, figsize=(n_per_group*3, len(file.keys())*2))
    for i, group in enumerate(file.keys()):
        vicinal_results = [ds for ds in file[group].keys() if not ds.endswith("__coordinates")]
        for ii, dist in enumerate(vicinal_results):
            if n_per_group is not None and ii >= n_per_group:
                continue
            coordinates = file[group][dist+"__coordinates"]
            distribution = file[group][dist]
            axes[i,ii].scatter(coordinates[:,0], coordinates[:,1], c=distribution, norm=norm, cmap=palette)
            axes[i, ii].set_title(f"{group} ({ii})")
            axes[i,ii].tick_params(bottom=False, labelbottom=False, left=False, labelleft=False)
    cbar = fig.colorbar(ScalarMappable(norm=norm, cmap=palette), ax=axes[:,:], shrink=0.8, label='Score', spacing='proportional')
    return fig
            

def set_params(plot:str):
    """
    Sets figure style parameters.

    Arguments
    =========
    plot
        The type of plot being created (composition, performance or region).
    
    """
    rcParams['font.size'] = 12
    rcParams['axes.labelsize'] = 16
    rcParams['axes.titlepad'] = 10
    rcParams['axes.titlesize'] = 18
    # rcParams['axes.axisbelow'] = True
    rcParams['ytick.major.size'] = 0
    rcParams['ytick.minor.size'] = 0
    rcParams['xtick.major.size'] = 0
    rcParams['xtick.minor.size'] = 0
    rcParams['axes.spines.left'] = False
    rcParams['axes.spines.right'] = False
    rcParams['axes.spines.top'] = True
    rcParams['axes.linewidth'] = 2
    rcParams['axes.edgecolor'] = 'grey'
    if plot == 'composition':
        rcParams['axes.spines.bottom'] = False
        rcParams['axes.labelpad'] = 10
    
        
    
