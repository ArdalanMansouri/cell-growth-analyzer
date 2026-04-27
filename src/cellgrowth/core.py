import pandas as pd
import plotly.express as px
import string

#%%
def map_num_to_letter(df: pd.DataFrame, col: str = 'Row', 
                      inplace: bool = True):
    """
    Maps integer row numbers (1-26) to uppercase alphabet letters.

    Args:
        df (pd.DataFrame): Input DataFrame.
        col (str): Column to remap. Defaults to 'Row'.
        inplace (bool): Modify df in place (True) or return a copy (False).

    Returns:
        pd.DataFrame 
    """

    row_map = {
        i: letter for i, 
               letter in enumerate(string.ascii_uppercase, start=1)
    }

    mapped = df[col].map(row_map) # Map the column values using the row_map

    if inplace:
        df[col] = mapped
        return None
    else:
        result = df.copy()
        result[col] = mapped
        return result
    
#%%
def sample_order_sorter(
    df, 
    desired_sample_order:list, 
    samples_col:str, 
    other_sort_para=False
):
    """ Re-arrange the order of the samples in the df and return a new df.
    
    Args:
        df: A pandas dataframe containing the data to be processed.
        desired_sample_order: Should be a list of string corresponding to the 
            name of samples.
        samples_col: The column with the name of samples.
        other_sort_para: List of other columns that should be used for sorting.
    
    Returns:
        A pandas dataframe with the samples in the desired order.
    """

    samples_order = desired_sample_order
    index_generator = dict(zip(samples_order, range(1, len(samples_order)+1)))
    df['Samples_order'] = df[samples_col].map(index_generator)
    if other_sort_para:
        df_new = df.sort_values(['Samples_order', *other_sort_para])
    else:
        df_new = df.sort_values(['Samples_order'])
    return df_new


class DataProcessing:
    def __init__(self, df: pd.DataFrame):
        """
        Initialize the DataProcessing class with a dataframe.
        Args:
            df: A pandas dataframe containing the data to be processed.
        """
        self.df = df

    def process_timepoints(
        self, 
        timepoint_col: str = 'Timepoint', 
        time_col: str = 'Time [s]'
    ):
        """
        For each timepoint, calculate the average time in hours, sort wells, 
        and create a new dataframe.
        Args:   
            timepoint_col: The name of the column in the dataframe that 
                contains the timepoint information. Default is 'Timepoint'.
            time_col: The name of the column in the dataframe that contains the 
                      time information in seconds. Default is 'Time [s]'.
        Returns:
            A pandas dataframe with the processed data, including a new column 
            for hours and sorted by Row and Column on the plate. 
        """
        list_df = []
        for unique in self.df[timepoint_col].unique():
            temp_data = self.df.loc[self.df[timepoint_col] == unique].copy()
            time = temp_data[time_col].mean()
            hour = round(time / 3600)
            temp_data.loc[:, "Hours"] = hour + 4
            temp_data = temp_data.sort_values(by=["Row", "Column"])
            list_df.append(temp_data)
        self.df = pd.concat(list_df, ignore_index=True)
        self.df.loc[self.df[timepoint_col] == 0, "Hours"] = 4
        return self.df

    def grouped(self):
        """
        Generate new columns for error bars and create a grouped statistics 
        table.

        Args:
            numerical_columns: List of numerical columns to calculate mean.
            cols_for_std: List of columns to calculate standard deviation.
        Returns:
            A pandas dataframe with grouped statistics.
        """


        self.df["cell_covered_area_std"] = self.df[
            "Texture A Selected - Region Area [µm²] - Sum per Well"
        ].copy()

        self.df["cell_count_std"] = self.df[
            "Cells Selected - Number of Objects"
        ].copy()

        numerical_columns = self.df.select_dtypes(
            exclude=object
        ).columns.to_list() 
        cols_for_std = ["cell_covered_area_std", "cell_count_std"]

        # Group by "Sample" and "Timepoint" and calculate statistics
        grouped_df = self.df.groupby(by=["Sample", "Timepoint"]).agg(
            {
                **{col: "mean" for col in numerical_columns 
                   if col != "Timepoint"},
                **{col: "std" for col in cols_for_std},
            }
        )

        grouped_df.reset_index(inplace=True)
        return grouped_df



#%%
class Graph:
    """A class for building and customizing Plotly line graphs.

    Attributes:
        xaxis_params: Dict of parameters applied to the x-axis via 
            update_xaxes().
        yaxis_params: Dict of parameters applied to the y-axis via 
            update_yaxes().
        layout_params: Dict of parameters applied to the figure layout.
        toggle_params: Dict of positional/display parameters for the toggle 
            button.
        fig: The active Plotly figure, set after calling line_graph().
    """

    def __init__(self):
        self.xaxis_params = {
            "showline": True,
            "linewidth": 2,
            "linecolor": "black",
            "mirror": True,
            "ticks": "outside",
            "title_text": "Hours",
            "range": (0, 100),
            "tickfont": dict(family="Arial", size=20),
            "title_font": dict(family="Arial", size=20),
        }
        self.yaxis_params = {
            "showline": True,
            "linewidth": 2,
            "linecolor": "black",
            "mirror": True,
            "ticks": "outside",
            "title_text": "",
            "tickfont": dict(family="Arial", size=20),
            "title_font": dict(family="Arial", size=20),
        }
        self.layout_params = {
            "plot_bgcolor": "white",
            "title": dict(text="", x=0.5),
            "font": dict(family="Arial", size=14, color="black"),
        }
        # Positional and display settings for the toggle button
        self.toggle_params = {
            "type": "buttons",
            "showactive": True,
            "x": 1.15,
            "y": 0.7,
            "xanchor": "right",
            "yanchor": "top",
        }
        self.fig = None

    def line_graph(
        self,
        df_grouped: pd.DataFrame,
        x: str,
        y: str,
        color: str = "Sample",
        
        color_discrete_map: dict = None,
        markers: bool = True,
        hover_data: list = None,
        error_y: str = None,
        width: int = 1200,
        height: int = 600,
        y_axis_ratios: bool = False,
    ):
        """Create a line graph and apply the stored axis and layout parameters.

        Args:
            df_grouped: Grouped dataframe used as the data source for the graph.
            x: Column name for the x-axis.
            y: Column name for the y-axis.
            color: Column name used to differentiate traces by colour.
            color_discrete_map: Dict mapping category values to colour strings.
            markers: Whether to show markers on the lines. Default True.
            hover_data: List of column names to include in the hover tooltip.
            error_y: Column name to use as the y-axis error bar.
            width: Figure width in pixels. Default 1200.
            height: Figure height in pixels. Default 600.
            y_axis_ratios: If True, normalise y values as ratios relative to 
                each group's first timepoint value. Default False.

        Returns:
            plotly.graph_objects.Figure
        """
        if color_discrete_map is None:
            color_discrete_map = {
                "Neg Control": "black",
                "Parental": "green",
                "LOW_uptake": "blue",
                "HIGH_uptake": "red",
            }

        if hover_data is None:
            hover_data = [
                "Texture A Selected - Region Area [µm²] - Sum per Well", 
                "Timepoint"
            ]

        if y_axis_ratios:
            ratios_list = []
            for group in df_grouped[color].unique():
                data = df_grouped.loc[df_grouped[color] == group]
                data = data.reset_index()
                series = data[y]
                ratios = [
                    series[i] / series[0] 
                    for i, _ in enumerate(series) if i > 0
                ]
                ratios.insert(0, 1)
                data["Ratios"] = ratios
                ratios_list.append(data)
            df_grouped = pd.concat(ratios_list)
            y = "Ratios"

        # Use the exact hours from the original dataframe as x-axis tick marks
        self.xaxis_params["tickvals"] = df_grouped[x].to_numpy()

        self.fig = px.line(
            df_grouped,
            x=x,
            y=y,
            color=color,
            color_discrete_map=color_discrete_map,
            markers=markers,
            hover_data=hover_data,
            error_y=error_y,
            width=width,
            height=height,
        )
        self.fig.update_xaxes(**self.xaxis_params)
        self.fig.update_yaxes(**self.yaxis_params)
        self.fig.update_layout(**self.layout_params)
        return self.fig

    def update_parameters(self, xaxis: dict = None, yaxis: dict = None, 
                          layout: dict = None):
        """Update any stored axis or layout parameters and apply them to 
        the figure.

        Each argument is a dict whose keys match Plotly's update_xaxes /
        update_yaxes / update_layout keyword arguments.  Calling this method
        both persists the new values in the class attributes and, if a figure
        already exists, applies them immediately.

        Args:
            xaxis: Dict of x-axis parameter overrides.
            yaxis: Dict of y-axis parameter overrides.
            layout: Dict of layout parameter overrides.

        Returns:
            plotly.graph_objects.Figure, or None if line_graph() has not been 
            called yet.
        """
        if xaxis:
            self.xaxis_params.update(xaxis)
            if self.fig is not None:
                self.fig.update_xaxes(**xaxis)
        if yaxis:
            self.yaxis_params.update(yaxis)
            if self.fig is not None:
                self.fig.update_yaxes(**yaxis)
        if layout:
            self.layout_params.update(layout)
            if self.fig is not None:
                self.fig.update_layout(**layout)
        return self.fig

    def add_toggle(self, df_grouped, error_col: str, 
                   color_col: str, show: bool = True):
        """Dynamically add or remove the error-bar toggle button from the 
        figure.

        Args:
            df_grouped: Grouped dataframe that contains the error column.
            error_col: Name of the column holding the error-bar values.
            color_col: Name of the column used to split traces (e.g. "Sample").
            show: If True, add the toggle; if False, remove it. Default True.

        Returns:
            plotly.graph_objects.Figure
        """
        if not show:
            self.fig.update_layout(updatemenus=[])
            return self.fig

        # Build one error_y dict per unique category, in the order they appear
        samples = df_grouped[color_col].unique()
        error_y_on = [
            dict(
                type="data",
                array=df_grouped.loc[
                    df_grouped[color_col] == sample, error_col
                ].tolist(),
            )
            for sample in samples
        ]

        updatemenus = [
            {
                "active": 0,
                "buttons": [
                    {
                        "method": "update",
                        "label": "error-bar display",
                        # args:  called on first click — restores error bars
                        "args": [{"error_y": error_y_on}],
                        # args2: called on second click — hides error bars
                        "args2": [{"error_y": dict(type="data", array=[])}],
                        "visible": True,
                    }
                ],
                **self.toggle_params,
            }
        ]

        self.fig.update_layout(updatemenus=updatemenus)
        return self.fig
    

