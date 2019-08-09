(* https://www.wolfram.com/language/11/cloud-and-web-interfaces/create-a-web-form-to-compute-the-marginal-tax-rate.html?product=language *)

AskFunction[Module[{bracket, tax, income},
   bracket = 
    Ask[{"brackets", 
       "What is your marital status?"} -> {"Married filing jointly" -> {18550, 75300, 151900, 231450, 413350, 466950}, 
       "Single" -> {9275, 37650, 91150, 190150, 413350, 415050}, 
       "Head of household" -> {13250, 50400, 130150, 210800, 413350, 
         441000}, 
       "Married filing separately" -> {9275, 37650, 75950, 115725, 
         206675, 233475}}];
   income = 
    Ask[{"income", "What was your income in the last year?"} -> 
      Restricted["Number", {0, Infinity}]];
   tax = Integrate[
     Piecewise[{{.10 , 0 <= x <= bracket[[1]]}, {.15, 
        bracket[[1]] < x <= bracket[[2]]}, {.25, 
        bracket[[2]] < x <= bracket[[3]]}, {.28, 
        bracket[[3]] < x <= bracket[[4]]}, {.33, 
        bracket[[4]] < x <= bracket[[5]]}, {.35, 
        bracket[[5]] < x <= bracket[[6]]}, {.396, True}}], {x, 0, 
      income - 
       If[Ask[{"deps", 
           "Do you have any dependents?"} -> {"Yes" -> True, 
           "No" -> False}], 
        Ask[{"nodeps", "How many?"} -> 
           Restricted["Integer", {0, Infinity}]]* 4050, 0]}];
   AskTemplateDisplay[
    Column[{"You owe $" <> TextString[tax] <> " in taxes.", 
       "Your marginal tax rate is " <> 
        TextString[Round[100.*tax/#income, 0.1]] <> "%", 
       PieChart[{tax, income}]}] &]
   ]]