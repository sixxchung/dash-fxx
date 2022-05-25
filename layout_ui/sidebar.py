import dash_bootstrap_components as dbc
from dash import dcc, html 
import dash_admin_components as dac

# Sidebar

sideMenu = 	dac.SidebarMenu(
    [
        dac.SidebarHeader(children="Cards"),
        dac.SidebarMenuItem(id='menu_basic_cards',  label='Basic cards',  icon='box'),

    ]
)
sidebar = dac.Sidebar(
    sideMenu,
    title='Alyx Admin',
	skin="dark",
    color="primary",
	brand_color="primary",
    url="https://onesixx.com",
    #src="https://adminlte.io/themes/AdminLTE/dist/img/user2-160x160.jpg",
    src="assets/user-01.jpg",
    elevation=3,
    opacity=0.8
)
