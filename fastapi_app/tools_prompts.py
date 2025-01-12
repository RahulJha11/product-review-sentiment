tools = [
    {
        "name": "extract_product_info_sentiment",
        "description": "Extracts key information from the product review text and the sentiment of the review.",
        "input_schema": {
            "type": "object",
            "properties": {
              "Product_details": {
                "type": "array",
                "items":{
                  "type": "object",
                  "property": {
                          "product_name": {"type": "string", "description": "Name of the product"},
                          "tpye": {"type": "string", "description": "type of the product. i.e product is belong to which cegogery"},
                          "price": {"type": "string", "description": "Price of the product. plese do not include any currency symbol"},
                          "discount": {"type": "string", "description": "Discount on the price. plese do not include any currency symbol"}
                                     }
                }
                         
               },

              "review_sentiment": {
                "type": "object",
                "items": {
                  "type": "object",
                "property":{
                  "sentiment": {"type": "string", "description": "sentiment of the producr review. Positive, Neutral, or Negative"}
                }
              },
        
                
            "required": ["product_name", "tpye", "price", "discount", "sentiment"]
        },
    }
        },
        "cache_control": {"type": "ephemeral"}
    }
    
]

prompt = """
  Analyze the product review text and extract the information in the below following format:

   {
  "Product_details": [
  {
    "product_name": "",
    "tpye": "",
    "price": "",
    "discount": ""
  },
  {
    "product_name": "",
    "tpye": "",
    "price": "",
    "discount": ""
  },
  {
    "product_name": "",
    "tpye": "",
    "price": "",
    "discount": ""
  }

  ],

  "review_sentiment": 
    {
      "quantity": ""
    }

  }

  Use the extract_product_info_&_sentiment tool to provide the extracted information exactly as mention format above. If review text has multiple product then add accordiningly into Product_details list.  If the data missing still return using the tool with values of empty string.
 
  Here's the product review text:
  [TEXT]
  """
