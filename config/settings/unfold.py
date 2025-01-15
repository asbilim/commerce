from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _

UNFOLD = {
    "SITE_TITLE": "Commercial Admin",  # Title in the browser tab
    "SITE_HEADER": "My Global Shop",  # Sidebar header title
    "INDEX_TITLE": "Dashboard",  # Fixed typo from "INDEX8TITLE" to "INDEX_TITLE"
    "SITE_URL": "/",  # Link for "View Site" button
    "SITE_ICON": {
        "light": lambda request: "https://cdn-icons-png.flaticon.com/512/833/833314.png",  # General business icon
        "dark": lambda request: "https://cdn-icons-png.flaticon.com/512/833/833316.png",
    },
    "SITE_LOGO": {
        "light": lambda request: "https://via.placeholder.com/150x50?text=Commercial+Light",  # Replace with a light logo
        "dark": lambda request: "https://via.placeholder.com/150x50?text=Commercial+Dark",   # Replace with a dark logo
    },
    "SITE_SYMBOL": "business",  # Material symbol
    "SITE_FAVICONS": [
        {
            "rel": "icon",
            "sizes": "32x32",
            "type": "image/png",
            "href": lambda request: "https://cdn-icons-png.flaticon.com/512/833/833314.png",
        },
    ],
    "SHOW_HISTORY": True,  # Enable history tracking in admin
    "SHOW_VIEW_ON_SITE": True,  # Enable "View on Site" button
    "ENVIRONMENT": "config.environment_callback",  # Dynamically determine environment
    "THEME": None,  # Default theme with light/dark switcher
    "LOGIN": {
        "image": lambda request: "https://via.placeholder.com/1920x1080?text=Welcome+to+Commercial",  # Background for login page
        "redirect_after": lambda request: reverse_lazy("admin:index"),  # Redirect after login
    },
    "STYLES": [
        lambda request: "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css",  # Include FontAwesome
    ],
    "SCRIPTS": [
        lambda request: "https://cdnjs.cloudflare.com/ajax/libs/Chart.js/3.9.1/chart.min.js",  # Example JS library for charts
    ],
    "COLORS": {
        "font": {
            "subtle-light": "107 114 128",
            "subtle-dark": "156 163 175",
            "default-light": "75 85 99",
            "default-dark": "209 213 219",
            "important-light": "17 24 39",
            "important-dark": "243 244 246",
        },
        "primary": {
            "50": "250 245 255",
            "100": "243 232 255",
            "200": "233 213 255",
            "300": "216 180 254",
            "400": "192 132 252",
            "500": "168 85 247",
            "600": "147 51 234",
            "700": "126 34 206",
            "800": "107 33 168",
            "900": "88 28 135",
            "950": "59 7 100",
        },
    },
    "EXTENSIONS": {},
    "SIDEBAR": {
        "show_search": True,  # Enable search
        "show_all_applications": True,  # Enable dropdown for all apps
        "navigation": [
            {
                "title": _("Main Navigation"),
                "separator": True,
                "collapsible": True,
                "items": [
                    {
                        "title": _("Dashboard"),
                        "icon": "dashboard",
                        "link": reverse_lazy("admin:index"),
                    },
                    {
                        "title": _("Users"),
                        "icon": "people",
                        "link": reverse_lazy("admin:users_user_changelist"),  # Updated link
                    },
                ],
            },
        ],
    },
    "TABS": [],
}
