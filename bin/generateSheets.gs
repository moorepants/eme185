// Generate sheets from given names in column A of sheet 1 and template rubric on sheet 2

function generateSheets() {
  // set ss object as active googledoc
  var ss = SpreadsheetApp.getActiveSpreadsheet();
  // save template sheet as second sheet
  var templateSheet = ss.getSheets()[1];
  // save team name sheet for first sheet
  var teamNameSheet = ss.getSheets()[0];
  // store team names in arrays
  var teamID = teamNameSheet.getRange("A1:A17").getValues();
  var teamName = teamNameSheet.getRange("B1:B17").getValues();

  var sheetNumber, sourceSheet, newSheetName;

  // iterate through all sheets in the spreadsheet
  for( sheetNumber = teamName.length; sheetNumber < teamName.length +1; sheetNumber++) {
    // Duplicate sheet
    ss.setActiveSheet(templateSheet);
    ss.duplicateActiveSheet();
    ss.renameActiveSheet(teamName[sheetNumber])

    sourceSheet = ss.getActiveSheet();
    // Place Team name at top and rename sheet
    sourceSheet.getRange('b1').setValue(teamName[sheetNumber])
    sourceSheet.setName(teamName[sheetNumber]);


  }
}

