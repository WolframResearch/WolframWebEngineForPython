FormFunction[
    {"image" -> "Image", "filter" -> ImageEffect[]}, 
    ImageEffect[#image, #filter] &,
    "PNG",
    AppearanceRules -> <|
        "Title" -> "Welcome to WolframWebEngine",
        "Description" -> TemplateApply["This is a sample application running on a `` Kernel.", $VersionNumber]
    |>
]