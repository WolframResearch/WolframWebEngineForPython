FormPage[
    {"From" -> "City", "To" -> "City"}, 
    GeoGraphics[
        Style[Line[TravelDirections[{#From, #To}]], Thick, Red]
    ] &, 
    AppearanceRules -> <|
        "Title" -> "Get travel directions for your trip",
        "Description" -> TemplateApply["This is a sample application running on a `` Kernel.", $VersionNumber]
    |>
]