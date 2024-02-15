#Dette scriptet genererer treningsdata

import urllib.parse

def generate_wms_getmap_url():

    # Base URL of the WMS service
    base_url = "https://openwms.statkart.no/skwms1/wms.fkb"
    
    # Common WMS parameters with static values
    wms_params = {
        'SERVICE': 'WMS',
        'VERSION': '1.3.0',
        'REQUEST': 'GetMap',
        'BBOX': '86862.34650433670322,6466039.970492540859,87579.68362640209671,6466748.95569468569',
        'CRS': 'EPSG:25833',
        'WIDTH': '774',
        'HEIGHT': '764',
        'LAYERS': '',
        'STYLES': '',
        'FORMAT': 'image/png',
        'DPI': '96',
        'MAP_RESOLUTION': '96',
        'FORMAT_OPTIONS': 'dpi:96',
        'TRANSPARENT': 'false',
        'sld_body': ''
    }

    # Ask user for input for layers
    layer_names = input("Enter LAYERS (layer names, comma-separated if multiple, Current layers are: veg,bru,bygning): ")
    wms_params['LAYERS'] = layer_names
    

    # Start the SLD body
    sld_body = '''
<sld:StyledLayerDescriptor version="1.0.0" xmlns:sld="http://www.opengis.net/sld" xmlns:ogc="http://www.opengis.net/ogc" xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.opengis.net/sld StyledLayerDescriptor.xsd">
'''
    
    # Generate a NamedLayer block for each layer
    for layer_name in layer_names.split(','):
        sld_body += f'''
    <sld:NamedLayer>
        <sld:Name>{layer_name.strip()}</sld:Name>
        <sld:UserStyle>
            <sld:FeatureTypeStyle>
                <sld:Rule>
                    <sld:MinScaleDenominator>0</sld:MinScaleDenominator>
                    <sld:MaxScaleDenominator>999999999</sld:MaxScaleDenominator>
                    <PolygonSymbolizer>
                        <Fill>
                            <CssParameter name="fill">#000000</CssParameter>
                        </Fill>
                    </PolygonSymbolizer>
                </sld:Rule>
            </sld:FeatureTypeStyle>
        </sld:UserStyle>
    </sld:NamedLayer>
'''
    
    # Close the SLD body
    sld_body += '</sld:StyledLayerDescriptor>'
    
    # Assign the complete SLD body to the wms_params
    wms_params['sld_body'] = sld_body
    
    # Encode parameters, including SLD body
    encoded_params = urllib.parse.urlencode(wms_params, quote_via=urllib.parse.quote)

    # Build and print the full URL
    full_url = f"{base_url}?{encoded_params}"
    print("Generated URL:")
    print(full_url)

    # Return the full URL
    return full_url

# Generate the URL
generated_url = generate_wms_getmap_url()