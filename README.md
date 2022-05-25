# dash-fxx

# example> add menu stock plot

-1- make a new folder(stock) for dash
dashPages/stock
dashPages/stock/view.py
dashPages/stock/model.py
dashPages/stock/callbacks.py


-2- insert view link to /ui/main_content.py
import dashPages.stock.view
body = dac.Body(
    dac.TabItems([
        #dashPages.home.view.content,
        dashPages.stock.view.content,
    ])
)
-3- insert link to /ui/sidebar.py
sideMenu = 	dac.SidebarMenu(
    [ ...   
        dac.SidebarHeader(children="etc."),
        dac.SidebarMenuItem(id='menu_stock', label='Stock plot',  icon='desktop'),
    ]
)
-4- modify input, output callback /ui/sidebar_callbacks.py

MENU_ITEMS = ( "basic_cards", "social_cards", "tab_cards", 
               "basic_boxes", "value_boxes",
               "gallery_1", "gallery_2",
               "Stock")
def update_breadcrumbs( nClick1, nClick2, nClick3, nClick4, nClick5, nClick6, nClick7, nClick8,
    basic_cards, social_cards, tab_cards, basic_boxes, value_boxes, gallery_1, gallery_2, stock ): 


-5- insert callbacks link to /routes.py 
from dashPages.stock.callbacks import update_graph

