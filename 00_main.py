# Import packages
from dash import Dash

# Import local packages
import functions.data_prep as dp
from app.layout import layout_define
from app.callbacks import register_callbacks

# Stand up app
app = Dash(__name__)

# create data
activities = dp.import_data()

# App layout
app.layout = layout_define(activities)

# Register callbacks
register_callbacks(app, activities)

# Run the app
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8050)
