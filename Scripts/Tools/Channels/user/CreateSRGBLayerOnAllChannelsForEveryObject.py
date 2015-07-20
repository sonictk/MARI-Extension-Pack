import mari

mariGeoList = mari.geo.list()

for geo in mariGeoList:
    
    mariChannelList = geo.channelList()
    
    for channel in mariChannelList:
        SRGBtoLinearLayer = channel.createAdjustmentLayer("sRGB2Linear", "Filter/sRGB2Linear")