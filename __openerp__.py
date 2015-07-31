{
    'name': 'Ship',
    'version': '1.0',
    'category': 'Tools',
    'summary': 'Ship, Product sales, IMport and Export',
    'description': """
Ship, Product, Manufacture
================================

This module manages the ship attributes, the organization,
sales, and the manufacture of products.
""",
    'depends' : ['base','sale','purchase'],
    'data' : ['view/menu.xml',
              'view/mysale_order_wrkflow.xml',
              'security/ir.model.access.csv',
              'view/my_journel_field.xml',
              'view/report_samplereport.xml',
              'view/sale_report_test1.xml'],
    'images': [],
    'demo': [],
    'installable' : True,
    'application': True,
}