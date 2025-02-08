import requests
from pymongo import MongoClient
from pydantic import BaseModel, field_validator
from typing import Optional
import pandas as pd

client = MongoClient('localhost', 27017)

db = client["markets"]  
collection = db["products"]
collection.delete_many({}) 

class Utils:

    URL_D1 = 'https://domicilios.tiendasd1.com'
    API_MARKET = "https://nextgentheadless.instaleap.io/api/v3"

class Product(BaseModel):

    id : str 
    name : str 
    price : Optional[float]
    weight : Optional[float]
    link : Optional[str] 
    market : str
    categories : Optional[list]
    images : Optional[list]
    description : Optional[str]

    @field_validator('price')
    @classmethod
    def price_validation(cls,value):
        if value and value <= 0:
            raise ValueError("El precio debe ser mayor a 0")
        
        return value
    
    @field_validator('description')
    @classmethod
    def description_validation(cls,value):
        if value and len(value)<=3:
            raise ValueError("La descripción es muy corta")
        return value
    
    @field_validator('weight')
    @classmethod
    def weight_validation(cls,value):
        if value and value <= 0:
            raise ValueError("El peso del producto debe ser mayor a 0")
        
        return value


def get_categories():
    
    payload = [
                {
                    "operationName": "GetCategoryTree",
                    "variables": {"getCategoryInput": {
                            "clientId": "D1",
                            "storeReference": "11808"
                        }},
                    "query": "fragment CategoryFields on CategoryModel {\n  active\n  boost\n  hasChildren\n  categoryNamesPath\n  isAvailableInHome\n  level\n  name\n  path\n  reference\n  slug\n  photoUrl\n  imageUrl\n  shortName\n  isFeatured\n  isAssociatedToCatalog\n  __typename\n}\n\nfragment CategoriesRecursive on CategoryModel {\n  subCategories {\n    ...CategoryFields\n    subCategories {\n      ...CategoryFields\n      subCategories {\n        ...CategoryFields\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n  __typename\n}\n\nfragment CategoryModel on CategoryModel {\n  ...CategoryFields\n  ...CategoriesRecursive\n  __typename\n}\n\nquery GetCategoryTree($getCategoryInput: GetCategoryInput!) {\n  getCategory(getCategoryInput: $getCategoryInput) {\n    ...CategoryModel\n    __typename\n  }\n}"
                },
                {
                    "operationName": "getDynamicHome",
                    "variables": {"getDynamicHomeInput": {
                            "breakpointId": "xsmall-450",
                            "storeReference": "11808",
                            "targetType": "WEB",
                            "clientId": "D1"
                        }},
                    "query": "query getDynamicHome($getDynamicHomeInput: GetDynamicHomeInput!) {\n  getDynamicHome(getDynamicHomeInput: $getDynamicHomeInput)\n}"
                }
            ]
    
    
    data = requests.request("POST", url = Utils.API_MARKET, json=payload).json()

    return data[0]['data']['getCategory']
        
categories = get_categories()

products_list = list()

for category in categories:

    payload = [
        {
            "operationName": "GetProductsByCategory",
            "variables": {"getProductsByCategoryInput": {
                    "categoryReference": category['reference'],
                    "categoryId": "null",
                    "clientId": "D1",
                    "storeReference": "11808",
                    "currentPage": 1,
                    "pageSize": 1000,
                    "filters": {},
                    "googleAnalyticsSessionId": ""
                }},
        "query": "fragment CategoryFields on CategoryModel {\n  active\n  boost\n  hasChildren\n  categoryNamesPath\n  isAvailableInHome\n  level\n  name\n  path\n  reference\n  slug\n  photoUrl\n  imageUrl\n  shortName\n  isFeatured\n  isAssociatedToCatalog\n  __typename\n}\n\nfragment CatalogProductTagModel on CatalogProductTagModel {\n  description\n  enabled\n  textColor\n  filter\n  tagReference\n  backgroundColor\n  name\n  __typename\n}\n\nfragment CatalogProductFormatModel on CatalogProductFormatModel {\n  format\n  equivalence\n  unitEquivalence\n  clickMultiplier\n  minQty\n  maxQty\n  __typename\n}\n\nfragment Taxes on ProductTaxModel {\n  taxId\n  taxName\n  taxType\n  taxValue\n  taxSubTotal\n  __typename\n}\n\nfragment PromotionCondition on PromotionCondition {\n  quantity\n  price\n  priceBeforeTaxes\n  taxTotal\n  taxes {\n    ...Taxes\n    __typename\n  }\n  __typename\n}\n\nfragment Promotion on Promotion {\n  type\n  isActive\n  conditions {\n    ...PromotionCondition\n    __typename\n  }\n  description\n  endDateTime\n  startDateTime\n  __typename\n}\n\nfragment PromotedModel on PromotedModel {\n  isPromoted\n  onLoadBeacon\n  onClickBeacon\n  onViewBeacon\n  onBasketChangeBeacon\n  onWishlistBeacon\n  __typename\n}\n\nfragment SpecificationModel on SpecificationModel {\n  title\n  values {\n    label\n    value\n    __typename\n  }\n  __typename\n}\n\nfragment NutritionalDetailsInformation on NutritionalDetailsInformation {\n  servingName\n  servingSize\n  servingUnit\n  servingsPerPortion\n  nutritionalTable {\n    nutrientName\n    quantity\n    unit\n    quantityPerPortion\n    dailyValue\n    __typename\n  }\n  bottomInfo\n  __typename\n}\n\nfragment CatalogProductModel on CatalogProductModel {\n  name\n  price\n  photosUrl\n  unit\n  subUnit\n  subQty\n  description\n  sku\n  ean\n  maxQty\n  minQty\n  clickMultiplier\n  nutritionalDetails\n  isActive\n  slug\n  brand\n  stock\n  securityStock\n  boost\n  isAvailable\n  location\n  priceBeforeTaxes\n  taxTotal\n  promotion {\n    ...Promotion\n    __typename\n  }\n  taxes {\n    ...Taxes\n    __typename\n  }\n  categories {\n    ...CategoryFields\n    __typename\n  }\n  categoriesData {\n    ...CategoryFields\n    __typename\n  }\n  formats {\n    ...CatalogProductFormatModel\n    __typename\n  }\n  tags {\n    ...CatalogProductTagModel\n    __typename\n  }\n  specifications {\n    ...SpecificationModel\n    __typename\n  }\n  promoted {\n    ...PromotedModel\n    __typename\n  }\n  score\n  relatedProducts\n  ingredients\n  stockWarning\n  nutritionalDetailsInformation {\n    ...NutritionalDetailsInformation\n    __typename\n  }\n  productVariants\n  isVariant\n  isDominant\n  __typename\n}\n\nfragment CategoryWithProductsModel on CategoryWithProductsModel {\n  name\n  reference\n  level\n  path\n  hasChildren\n  active\n  boost\n  isAvailableInHome\n  slug\n  photoUrl\n  categoryNamesPath\n  imageUrl\n  shortName\n  isFeatured\n  products {\n    ...CatalogProductModel\n    __typename\n  }\n  __typename\n}\n\nfragment PaginationTotalModel on PaginationTotalModel {\n  value\n  relation\n  __typename\n}\n\nfragment PaginationModel on PaginationModel {\n  page\n  pages\n  total {\n    ...PaginationTotalModel\n    __typename\n  }\n  __typename\n}\n\nfragment AggregateBucketModel on AggregateBucketModel {\n  min\n  max\n  key\n  docCount\n  __typename\n}\n\nfragment AggregateModel on AggregateModel {\n  name\n  docCount\n  buckets {\n    ...AggregateBucketModel\n    __typename\n  }\n  __typename\n}\n\nfragment BannerModel on BannerModel {\n  id\n  storeId\n  title\n  desktopImage\n  mobileImage\n  targetUrl\n  targetUrlInfo {\n    type\n    url\n    __typename\n  }\n  targetCategory\n  index\n  categoryId\n  __typename\n}\n\nquery GetProductsByCategory($getProductsByCategoryInput: GetProductsByCategoryInput!) {\n  getProductsByCategory(getProductsByCategoryInput: $getProductsByCategoryInput) {\n    category {\n      ...CategoryWithProductsModel\n      __typename\n    }\n    pagination {\n      ...PaginationModel\n      __typename\n    }\n    aggregates {\n      ...AggregateModel\n      __typename\n    }\n    banners {\n      ...BannerModel\n      __typename\n    }\n    promoted {\n      ...PromotedModel\n      __typename\n    }\n    __typename\n  }\n}"
        }
    ]

    data = requests.request("POST", url=Utils.API_MARKET, json=payload).json()

    products = data[0]['data']['getProductsByCategory']['category']['products']


    for index,product in enumerate(products):
        payload_product = Product(
                                    id = product['sku'],
                                    name = product['name'],
                                    price = product['price'],
                                    weight = product['subQty'] if product['subUnit']=='g' else None ,
                                    link = Utils.URL_D1 + '/p/' + product['slug'] ,
                                    market = 'D1',
                                    categories = [category['name'] for category in product['categories']],
                                    images = product['photosUrl'],
                                    description = product['description']
                                )
        
        dict_event = payload_product.model_dump()
        products_list.append(dict_event)
        collection.insert_one(dict_event)
        print(f'PRODUCTO {index+1} DE {category['reference']} INSERTADO EXITOSAMENTE')

products_dataframe = pd.DataFrame(products_list)

products_dataframe.to_csv('products_d1.csv',sep=';',index=False)

client.close()