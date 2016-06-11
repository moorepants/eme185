/**
 * Export one or all sheets in a spreadsheet as PDF files on user's Google Drive,
 * in same folder that contained original spreadsheet.
 *
 * Adapted from https://code.google.com/p/google-apps-script-issues/issues/detail?id=3579#c25
 *
 * @param {String}  optSSId       (optional) ID of spreadsheet to export.
 *                                If not provided, script assumes it is
 *                                sheet-bound and opens the active spreadsheet.
 * @param {String}  optSheetId    (optional) ID of single sheet to export.
 *                                If not provided, all sheets will export.
 */
function convertToPDF( optSSId, optSheetId ) {

  // If a sheet ID was provided, open that sheet, otherwise assume script is
  // sheet-bound, and open the active spreadsheet.
  var ss = (optSSId) ? SpreadsheetApp.openById(optSSId) : SpreadsheetApp.getActiveSpreadsheet();

  // Get URL of spreadsheet, and remove the trailing 'edit'
  var url = ss.getUrl().replace(/edit$/,'');

  // Get folder containing spreadsheet, for later export
  var parents = DriveApp.getFileById(ss.getId()).getParents();
  if (parents.hasNext()) {
    var folder = parents.next();
  }
  else {
    folder = DriveApp.getRootFolder();
  }

  // Get array of all sheets in spreadsheet
  var sheets = ss.getSheets();

  // Loop through all sheets, generating PDF files.
  for (var i=28; i < sheets.length ; i++) { //sheets.length
    var sheet = sheets[i];

    // If provided a optSheetId, only save it.
    if (optSheetId && optSheetId !== sheet.getSheetId()) continue;

    //additional parameters for exporting the sheet as a pdf
    var url_ext = 'export?exportFormat=pdf&format=pdf'   //export as pdf
        + '&gid=' + sheet.getSheetId()   //the sheet's Id
        // following parameters are optional...
        + '&size=letter'      // paper size
        + '&portrait=true'    // orientation, false for landscape
        + '&fitw=true'        // fit to width, false for actual size
        + '&sheetnames=false&printtitle=false&pagenumbers=false'  //hide optional headers and footers
        + '&gridlines=false'  // hide gridlines
        + '&fzr=false';       // do not repeat row headers (frozen rows) on each page

    var options = {
      headers: {
        'Authorization': 'Bearer ' +  ScriptApp.getOAuthToken()
      }
    }

    // Says response fails but files are still written to folder.
    var response = UrlFetchApp.fetch(url + url_ext, options);

    var blob = response.getBlob().setName( sheet.getName() + '-rubric.pdf');

    //from here you should be able to use and manipulate the blob to send and email or create a file per usual.
    //In this example, I save the pdf to drive
    folder.createFile(blob);
  }
}
