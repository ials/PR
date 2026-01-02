import ee

# Make sure EE is initialized before importing/using this module:
# ee.Initialize(project='your-ee-project-id')

# --------------------------------------------------------------------------------------------------
# PACE OCI wavelengths and band name helpers
# --------------------------------------------------------------------------------------------------

wl_pace_sr = [
    346, 351, 356, 361, 366, 371, 375, 380, 385, 390, 395, 400, 405, 410, 415, 420, 425, 430, 435, 440,
    445, 450, 455, 460, 465, 470, 475, 480, 485, 490, 495, 500, 505, 510, 515, 520, 525, 530, 535, 540,
    545, 550, 555, 560, 565, 570, 575, 580, 586, 615, 620, 625, 630, 635, 640, 642, 645, 647, 650, 652,
    655, 657, 660, 662, 665, 667, 670, 672, 675, 677, 679, 682, 697, 699, 702, 704, 707, 709, 712, 714,
    719, 724, 729, 734, 739, 742, 744, 747, 749, 752, 754, 772, 774, 779, 784, 789, 794, 799, 804, 809,
    814, 819, 824, 829, 835, 840, 845, 850, 855, 860, 865, 870, 875, 880, 885, 890, 895, 1038, 1249, 1618, 2131, 2258
]

wl_pace = wl_pace_sr
wl_pace_vnir = [
    346, 351, 356, 361, 366, 371, 375, 380, 385, 390, 395, 400, 405, 410, 415, 420, 425, 430, 435, 440,
    445, 450, 455, 460, 465, 470, 475, 480, 485, 490, 495, 500, 505, 510, 515, 520, 525, 530, 535, 540,
    545, 550, 555, 560, 565, 570, 575, 580, 586, 615, 620, 625, 630, 635, 640, 642, 645, 647, 650, 652,
    655, 657, 660, 662, 665, 667, 670, 672, 675, 677, 679, 682, 697, 699, 702, 704, 707, 709, 712, 714,
    719, 724, 729, 734, 739, 742, 744, 747, 749, 752, 754, 772, 774, 779, 784, 789, 794, 799, 804, 809,
    814, 819, 824, 829, 835, 840, 845, 850, 855, 860, 865, 870, 875, 880, 885, 890, 895
]

wl_pace_rrs = [
    346, 348, 351, 353, 356, 358, 361, 363, 366, 368, 371, 373, 375, 378, 380, 383, 385, 388, 390, 393, 395, 398,
    400, 403, 405, 408, 410, 413, 415, 418, 420, 422, 425, 427, 430, 432, 435, 437, 440, 442, 445, 447, 450,
    452, 455, 457, 460, 462, 465, 467, 470, 472, 475, 477, 480, 482, 485, 487, 490, 492, 495, 497,
    500, 502, 505, 507, 510, 512, 515, 517, 520, 522, 525, 527, 530, 532, 535, 537, 540, 542, 545, 547, 550,
    553, 555, 558, 560, 563, 565, 568, 570, 573, 575, 578, 580, 583, 586, 588,
    613, 615, 618, 620, 623, 625, 627, 630, 632, 635, 637, 640, 641, 642, 643, 645, 646, 647, 648, 650,
    651, 652, 653, 655, 656, 657, 658, 660, 661, 662, 663, 665, 666, 667, 668, 670, 671, 672, 673, 675,
    676, 677, 678, 679, 681, 682, 683, 684, 686, 687, 688, 689, 691, 692, 693, 694, 696, 697, 698, 699,
    701, 702, 703, 704, 706, 707, 708, 709, 711, 712, 713, 714, 717, 719
]

# (bands_oci_orig, bands_oci_mod, bands_oci_rrs_orig, bands_oci_rrs_mod, wl_modis, wl_modis_, etc.
# can be defined here exactly as lists, analogous to the JS file; omitted for brevity.)

# --------------------------------------------------------------------------------------------------
# EMIT collections and helpers
# --------------------------------------------------------------------------------------------------

wl_emit = [
    381.00558, 388.4092, 395.81583, 403.2254, 410.638, 418.0536, 425.47214, 432.8927, 440.31726, 447.7428, 455.17035,
    462.59888, 470.0304, 477.46292, 484.89743, 492.33292, 499.77142, 507.2099, 514.6504, 522.0909, 529.5333, 536.9768,
    544.42126, 551.8667, 559.3142, 566.7616, 574.20905, 581.6585, 589.108, 596.55835, 604.0098, 611.4622, 618.9146,
    626.36804, 633.8215, 641.2759, 648.7303, 656.1857, 663.6411, 671.09753, 678.5539, 686.0103, 693.4677, 700.9251,
    708.38354, 715.84094, 723.2993, 730.7587, 738.2171, 745.6765, 753.1359, 760.5963, 768.0557, 775.5161, 782.97754,
    790.4379, 797.89935, 805.36176, 812.8232, 820.2846, 827.746, 835.2074, 842.66986, 850.1313, 857.5937, 865.0551,
    872.5176, 879.98004, 887.44147, 894.90393, 902.3664, 909.82886, 917.2913, 924.7538, 932.21625, 939.6788, 947.14026,
    954.6027, 962.0643, 969.5268, 976.9883, 984.4498, 991.9114, 999.37286, 1006.8344, 1014.295, 1021.7566, 1029.2172,
    1036.6777, 1044.1383, 1051.5989, 1059.0596, 1066.5201, 1073.9797, 1081.4404, 1088.9, 1096.3597, 1103.8184, 1111.2781,
    1118.7368, 1126.1964, 1133.6552, 1141.1129, 1148.5717, 1156.0304, 1163.4882, 1170.9459, 1178.4037, 1185.8616, 1193.3184,
    1200.7761, 1208.233, 1215.6898, 1223.1467, 1230.6036, 1238.0596, 1245.5154, 1252.9724, 1260.4283, 1267.8833, 1275.3392,
    1282.7942, 1290.2502, 1297.7052, 1305.1603, 1312.6144, 1320.0685, 1327.5225, 1334.9756, 1342.4287, 1349.8818, 1357.3351,
    1364.7872, 1372.2384, 1379.6907, 1387.1418, 1394.5931, 1402.0433, 1409.4937, 1416.944, 1424.3933, 1431.8427, 1439.292,
    1446.7404, 1454.1888, 1461.6372, 1469.0847, 1476.5321, 1483.9796, 1491.4261, 1498.8727, 1506.3192, 1513.7649, 1521.2104,
    1528.655, 1536.1007, 1543.5454, 1550.9891, 1558.4329, 1565.8766, 1573.3193, 1580.7621, 1588.205, 1595.6467, 1603.0886,
    1610.5295, 1617.9705, 1625.4104, 1632.8513, 1640.2903, 1647.7303, 1655.1694, 1662.6074, 1670.0455, 1677.4836, 1684.9209,
    1692.358, 1699.7952, 1707.2314, 1714.6667, 1722.103, 1729.5383, 1736.9727, 1744.4071, 1751.8414, 1759.2749, 1766.7084,
    1774.1418, 1781.5743, 1789.007, 1796.4385, 1803.8701, 1811.3008, 1818.7314, 1826.1611, 1833.591, 1841.0206, 1848.4495,
    1855.8773, 1863.3052, 1870.733, 1878.16, 1885.5869, 1893.013, 1900.439, 1907.864, 1915.2892, 1922.7133, 1930.1375, 1937.5607,
    1944.9839, 1952.4071, 1959.8295, 1967.2518, 1974.6732, 1982.0946, 1989.515, 1996.9355, 2004.355, 2011.7745, 2019.1931, 2026.6118,
    2034.0304, 2041.4471, 2048.865, 2056.2808, 2063.6965, 2071.1123, 2078.5273, 2085.9421, 2093.3562, 2100.769, 2108.1821, 2115.5942,
    2123.0063, 2130.4175, 2137.8289, 2145.239, 2152.6482, 2160.0576, 2167.467, 2174.8755, 2182.283, 2189.6904, 2197.097, 2204.5034,
    2211.9092, 2219.3147, 2226.7195, 2234.1233, 2241.5269, 2248.9297, 2256.3328, 2263.7346, 2271.1365, 2278.5376, 2285.9387, 2293.3386,
    2300.7378, 2308.136, 2315.5342, 2322.9326, 2330.3298, 2337.7263, 2345.1216, 2352.517, 2359.9126, 2367.3071, 2374.7007, 2382.0935,
    2389.486, 2396.878, 2404.2695, 2411.6604, 2419.0513, 2426.4402, 2433.8303, 2441.2183, 2448.6064, 2455.9944, 2463.3816, 2470.7678,
    2478.153, 2485.5386, 2492.9238
]

# Full EMIT collection
coll_emit = ee.ImageCollection('NASA/EMIT/L2A/RFL').select(ee.List.sequence(0, 284))

# EMIT subset collection (exclude 128–143, 188–213)
coll_emit_sub = (
    ee.ImageCollection('NASA/EMIT/L2A/RFL')
    .select(
        ee.List.sequence(0, 126)
        .cat(ee.List.sequence(143, 186))
        .cat(ee.List.sequence(213, 284))
    )
)

# Rescaled EMIT collection (×10000, int16)
coll_emit_rescaled = (
    ee.ImageCollection('NASA/EMIT/L2A/RFL')
    .select(ee.List.sequence(0, 284))
    .map(lambda img: img.multiply(10000).toInt16()
         .set('system:time_start', img.get('system:time_start')))
)

# --------------------------------------------------------------------------------------------------
# EMIT single‑date and multi‑date helpers
# --------------------------------------------------------------------------------------------------

def emit_sr(roi, date):
    """Subset EMIT (243 bands, excluding bad bands) for a single date."""
    src = ee.ImageCollection('NASA/EMIT/L2A/RFL')
    img1 = (
        src.filterDate(ee.Date(date), ee.Date(date).advance(1, 'day'))
           .filterBounds(roi)
           .select(ee.List.sequence(0, 126))
           .median()
           .multiply(10000)
           .toInt16()
    )
    img2 = (
        src.filterDate(ee.Date(date), ee.Date(date).advance(1, 'day'))
           .filterBounds(roi)
           .select(ee.List.sequence(143, 186))
           .median()
           .multiply(10000)
           .toInt16()
    )
    img3 = (
        src.filterDate(ee.Date(date), ee.Date(date).advance(1, 'day'))
           .filterBounds(roi)
           .select(ee.List.sequence(213, 284))
           .median()
           .multiply(10000)
           .toInt16()
    )
    return (img1.addBands(img2)
                .addBands(img3)
                .set('system:time_start', img1.get('system:time_start')))

def emit_sr2(roi, date1, date2):
    """Subset EMIT (243 bands, excluding bad bands) for a date range."""
    src = ee.ImageCollection('NASA/EMIT/L2A/RFL')
    img1 = (
        src.filterDate(ee.Date(date1), ee.Date(date2))
           .filterBounds(roi)
           .select(ee.List.sequence(0, 126))
           .median()
           .multiply(10000)
           .toInt16()
           .clip(roi)
    )
    img2 = (
        src.filterDate(ee.Date(date1), ee.Date(date2))
           .filterBounds(roi)
           .select(ee.List.sequence(143, 186))
           .median()
           .multiply(10000)
           .toInt16()
           .clip(roi)
    )
    img3 = (
        src.filterDate(ee.Date(date1), ee.Date(date2))
           .filterBounds(roi)
           .select(ee.List.sequence(213, 284))
           .median()
           .multiply(10000)
           .toInt16()
           .clip(roi)
    )
    return img1.addBands(img2).addBands(img3)

def emit_sr_full(roi, date):
    """Full EMIT (0–284) for a single day."""
    return (
        ee.ImageCollection('NASA/EMIT/L2A/RFL')
        .filterDate(ee.Date(date), ee.Date(date).advance(1, 'day'))
        .filterBounds(roi)
        .select(ee.List.sequence(0, 284))
        .median()
        .multiply(10000)
        .toInt16()
    )

def emit_sr_bz(date):
    """Full EMIT over a fixed Belize ROI (from JS) for a single day."""
    roi = ee.Geometry.Rectangle(-87.28, 15.85, -89.27, 18.54)
    return (
        ee.ImageCollection('NASA/EMIT/L2A/RFL')
        .filterDate(ee.Date(date), ee.Date(date).advance(1, 'day'))
        .filterBounds(roi)
        .select(ee.List.sequence(0, 284))
        .median()
        .multiply(10000)
        .toInt16()
        .clip(roi)
    )

def emit_sr_full2(roi, date1, date2):
    """Full EMIT (0–284) for flexible date range."""
    return (
        ee.ImageCollection('NASA/EMIT/L2A/RFL')
        .filterDate(ee.Date(date1), ee.Date(date2))
        .filterBounds(roi)
        .select(ee.List.sequence(0, 284))
        .median()
        .multiply(10000)
        .toInt16()
    )

# --------------------------------------------------------------------------------------------------
# Simple EMIT rescale helper
# --------------------------------------------------------------------------------------------------

def rescale(img):
    """Divide reflectance image by 10000, keep system:time_start."""
    return img.divide(10000).set('system:time_start', img.get('system:time_start'))

# --------------------------------------------------------------------------------------------------
# Normalization
# --------------------------------------------------------------------------------------------------

def norm(img):
    """Min‑max normalize each band to [0,1] over image bounds."""
    band_names = img.bandNames()
    region = img.geometry().bounds()
    scale = img.projection().nominalScale()
    min_dict = img.reduceRegion(
        reducer=ee.Reducer.min(),
        geometry=region,
        scale=scale,
        maxPixels=1e9,
        bestEffort=True,
        tileScale=16
    )
    max_dict = img.reduceRegion(
        reducer=ee.Reducer.max(),
        geometry=region,
        scale=scale,
        maxPixels=1e9,
        bestEffort=True,
        tileScale=16
    )
    mins = ee.Image.constant(min_dict.values(band_names))
    maxs = ee.Image.constant(max_dict.values(band_names))
    return img.subtract(mins).divide(maxs.subtract(mins))

# --------------------------------------------------------------------------------------------------
# PCA (Ujaval’s implementation, translated)
# --------------------------------------------------------------------------------------------------

def pca(img):
    """PCA over image bounds; returns SD‑normalized PCs with variance props."""
    image = img.unmask()
    scale = img.projection().nominalScale()
    region = img.geometry().bounds()
    band_names = image.bandNames()

    mean_dict = image.reduceRegion(
        reducer=ee.Reducer.mean(),
        geometry=region,
        scale=scale,
        maxPixels=1e13,
        tileScale=16
    )
    means = ee.Image.constant(mean_dict.values(band_names))
    centered = image.subtract(means)

    def get_new_band_names(prefix):
        seq = ee.List.sequence(1, band_names.length())
        return seq.map(lambda b: ee.String(prefix).cat(ee.Number(b).int()))

    def get_principal_components(centered_img, scale_val, region_val):
        arrays = centered_img.toArray()
        covar = arrays.reduceRegion(
            reducer=ee.Reducer.centeredCovariance(),
            geometry=region_val,
            scale=scale_val,
            maxPixels=1e13,
            tileScale=16
        )
        covar_array = ee.Array(covar.get('array'))
        eigens = covar_array.eigen()
        eigen_values = eigens.slice(1, 0, 1)

        eigen_values_list = eigen_values.toList().flatten()
        total = eigen_values_list.reduce(ee.Reducer.sum())

        def _map_var(item):
            component = eigen_values_list.indexOf(item).add(1).format('%02d')
            variance = ee.Number(item).divide(total).multiply(100).format('%.2f')
            return ee.List([component, variance])

        percentage_variance = eigen_values_list.map(_map_var)
        variance_dict = ee.Dictionary(percentage_variance.flatten())

        eigen_vectors = eigens.slice(1, 1)
        array_image = arrays.toArray(1)
        principal_components = ee.Image(eigen_vectors).matrixMultiply(array_image)

        sd_image = (
            ee.Image(eigen_values.abs().sqrt())
            .arrayProject([0])
            .arrayFlatten([get_new_band_names('sd')])
        )

        return (
            principal_components
            .arrayProject([0])
            .arrayFlatten([get_new_band_names('pc')])
            .divide(sd_image)
            .set(variance_dict)
        )

    pc_image = get_principal_components(centered, scale, region)
    return pc_image.mask(img.mask())

def variance_pca(img):
    """Prints variance explained by PCs (server‑side; for debugging in Code Editor style)."""
    print('Variance of Principal Components', pca(img).toDictionary())

# --------------------------------------------------------------------------------------------------
# Simple drawing helpers (ln1, ln2)
# --------------------------------------------------------------------------------------------------

def ln1(roi):
    return ee.Image().byte().paint(featureCollection=roi, width=1)

def ln2(roi):
    return ee.Image().byte().paint(featureCollection=roi, width=2)
