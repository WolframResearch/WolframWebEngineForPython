(* https://www.wolfram.com/language/11/cloud-and-web-interfaces/add-an-arbitrary-number-of-fields-to-a-form.html?product=language *)

FormFunction[
  "city" -> RepeatingElement["City", {2, 5}], 
  GeoGraphics[
    Append[GeoMarker /@ #city, 
     Style[Line[TravelDirections[#city]], Thick, Red]], ImageSize -> 850] &, 
  AppearanceRules -> <|
    "Title" -> "Get travel directions for your trip"|>]