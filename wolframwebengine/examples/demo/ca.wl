(* https://www.wolfram.com/language/11/cloud-and-web-interfaces/create-a-complex-website-about-elementary-cellular.html?product=language *)

URLDispatcher @ {
   "/" ~~ EndOfString -> GalleryView[
     Table[
      Hyperlink[
       ArrayPlot[CellularAutomaton[i, {{1}, 0}, {50, All}]],
       "/ca/" <> 
        ToString[i]
       ],
      {i, {18, 22, 26, 28, 30, 50, 54, 45, 57, 73, 77, 60, 62, 105, 102, 126}}
      ]
     ],
    "/ca/" ~~ n : DigitCharacter .. ~~ EndOfString :> ExportForm[Column[{
       "Rule " <> n,
       RulePlot[CellularAutomaton[FromDigits[n]]],
       ArrayPlot[CellularAutomaton[FromDigits[n], {{1}, 0}, {50, All}]]
       }], "HTML"]
    }