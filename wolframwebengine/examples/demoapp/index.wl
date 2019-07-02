FormFunction[
    {"image" -> "Image", "filter" -> ImageEffect[]}, 
    ImageEffect[#image, #filter] &,
    "PNG",
    AppearanceRules -> <|
        "Title" -> "Welcome to Wolfram Web Engine",
        "Description" -> TemplateApply["This is a sample application running on a `` Kernel.", $VersionNumber]
    |>
]