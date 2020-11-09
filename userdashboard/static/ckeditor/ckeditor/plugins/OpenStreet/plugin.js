//Google map plugin by zmmaj from zmajsoft-team
//blah... version 2.
//problems? write to zmajsoft@zmajsoft.com

// Register a new CKEditor plugin.
// http://docs.cksource.com/ckeditor_api/symbols/CKEDITOR.resourceManager.html#add
//function to create and write API key to file

CKEDITOR.plugins.add( 'OpenStreet',
{
	// The plugin initialization logic goes inside this method.
	// http://docs.cksource.com/ckeditor_api/symbols/CKEDITOR.pluginDefinition.html#init
	init: function( editor )
	{
		// get API KEY
		var key =   jQuery.extend
    (
       {
          getValues: function(url) 
          {
              var result = null;
              $.ajax(
              {
                url: url,
                type: 'get',
                dataType: 'html',
                async: false,
                cache: false,
                success: function(data) 
                {
                    result = data;
                }
              });
          return result;
          }
       }
    );
 var key;   
    $.get("ckeditor/plugins/OpenStreet/key.txt")
    .done(function() { 
    key=$.getValues("ckeditor/plugins/OpenStreet/key.txt");   
var m=key.length;
if (m==0) key="";
    }).fail(function() { 
       key="";
    })
    


//document.getElementById("demo").innerHTML =myString;
		// Create an editor command that stores the dialog initialization command.
		// http://docs.cksource.com/ckeditor_api/symbols/CKEDITOR.command.html
		// http://docs.cksource.com/ckeditor_api/symbols/CKEDITOR.dialogCommand.html
		editor.addCommand( 'simpleLinkDialog', new CKEDITOR.dialogCommand( 'simpleLinkDialog' ) );
 
		// Create a toolbar button that executes the plugin command defined above.
		// http://docs.cksource.com/ckeditor_api/symbols/CKEDITOR.ui.html#addButton
		editor.ui.addButton( 'OpenStreet',
		{
			// Toolbar button tooltip.
			label: 'Insert a ZS OpenStreet version 1.3',
			// Reference to the plugin command name.
			command: 'simpleLinkDialog',
			// Button's icon file path.
			icon: this.path + 'images/gg.png'
		} );
 
		// Add a new dialog window definition containing all UI elements and listeners.
		// http://docs.cksource.com/ckeditor_api/symbols/CKEDITOR.dialog.html#.add
		// http://docs.cksource.com/ckeditor_api/symbols/CKEDITOR.dialog.dialogDefinition.html
		CKEDITOR.dialog.add( 'simpleLinkDialog', function( editor )
		{
			return {
				// Basic properties of the dialog window: title, minimum size.
				// http://docs.cksource.com/ckeditor_api/symbols/CKEDITOR.dialog.dialogDefinition.html
				title : 'ZmajSoft OpenStreet',
				minWidth : 400,
				minHeight : 200,
				// Dialog window contents.
				// http://docs.cksource.com/ckeditor_api/symbols/CKEDITOR.dialog.definition.content.html
						
				contents :
				[
					{
						
						// Definition of the Settings dialog window tab (page) with its id, label and contents.
						// http://docs.cksource.com/ckeditor_api/symbols/CKEDITOR.dialog.contentDefinition.html
						id : 'general',
						label : 'Settings',
                   title : 'ZmajSoft OpenStreet',
						elements :
						[
							// Dialog window UI element: HTML code field.
							// http://docs.cksource.com/ckeditor_api/symbols/CKEDITOR.ui.dialog.html.html
							{
								type : 'html',
								// HTML code to be shown inside the field.
								// http://docs.cksource.com/ckeditor_api/symbols/CKEDITOR.ui.dialog.html.html#constructor
								html : 'This dialog window lets you create and embed into text simple OpenStreet Map picture. </br> Click <a href="http://www.mapcoordinates.net/en" target="_blank"> -->HERE<--</a> to find Latitude/Longitude.'
							},
							//lets see a key
							{
								type : 'text',
								id : 'key',
								label : 'YOUR API Key',
                          default: key ,
                          size : '3',
								validate : CKEDITOR.dialog.validate.notEmpty( 'If is API EMPTY please go to </br> click <a href="https://developer.mapquest.com/plan_purchase/steps/business_edition/business_edition_free/register" target="_blank"> -->HERE<--</a> to GRAB your KEY' ),
								required : true,
								commit : function( data )
								{
									data.key = this.getValue();
								}
							},
							// Dialog window UI element: a text input field for the Latitude.
							// http://docs.cksource.com/ckeditor_api/symbols/CKEDITOR.ui.dialog.textInput.html
							{
								type : 'html',
                         html : ' ENTER position for first and second ( if you need second) marker </br> </br>---ENTER below data for FIRST (A)marker. '
							},
							{
								type : 'text',
								id : 'lat',
								label : 'Latitude',
                          default: '0' ,
                          size : '3',
								validate : CKEDITOR.dialog.validate.notEmpty( 'This marker (A) must have LATITUDE.' ),
								required : true,
								commit : function( data )
								{
									data.lat = this.getValue();
								}
							},
                   // Again same thing, this time for Longitude
						{
								type : 'text',
								id : 'lon',
								label : 'Longitude ',
                          default: '0' ,
								validate : CKEDITOR.dialog.validate.notEmpty( 'This marker (A) must have a LONGITUDE.' ),
								required : true,
								commit : function( data )
								{
									data.lon = this.getValue();
								}
							},
// Find color for first cursor
                     {
                       type : 'select',
                       id : 'color0',
                       label : 'Select marker icon ( default= mcenter)',
                       items : 
                    		[
									[ '<none>', 'mcenter' ],[ 'mcenter', 'mcenter' ],[ 'blue', 'blue-' ],[ 'purple', 'purple-' ],[ 'yellow', 'yellow-' ],
                             [ 'A', 'A' ],[ 'B', 'B' ],[ 'blue-1', 'blue_1-1' ],[ 'blue-2', 'blue_1-2' ],[ 'blue-s', 'blue-s' ],[ 'orange-s', 'orange-s' ],
                             [ 'blue_1-s', 'blue_1-s' ],[ 'orange_1-s', 'orange_1-s' ]],
							commit : function( data )
								{
									data.color0 = this.getValue();
								}
                         },
// SECOND MARKER
							{
								type : 'html',
                         html : ' <b>=====================================================</b></br> ENTER below data for SECOND (B) marker. '
							},
							{
								type : 'text',
								id : 'lat1',
								label : 'Latitude',
								required : false,
								default: '0' ,
								commit : function( data )
								{
									data.lat1 = this.getValue();
								}
							},
                   // Again same thing, this time for Longitude
						{
								type : 'text',
								id : 'lon1',
								label : 'Longitude ',
								required : false,
								default: '0' ,
								commit : function( data )
								{
									data.lon1 = this.getValue();
								}
							},
// Find color for second cursor
                     {
                       type : 'select',
                       id : 'color1',
                       label : 'Select marker Icon ( default= blue)',
                       items : 
                    		[
									[ '<none>', 'blue-' ],[ 'mcenter', 'mcenter' ],[ 'blue', 'blue-' ],[ 'purple', 'purple-' ],[ 'yellow', 'yellow-' ],
                             [ 'A', 'A' ],[ 'B', 'B' ],[ 'blue-1', 'blue_1-1' ],[ 'blue-2', 'blue_1-2' ],[ 'blue-s', 'blue-s' ],[ 'orange-s', 'orange-s' ],
                             [ 'blue_1-s', 'blue_1-s' ],[ 'orange_1-s', 'orange_1-s' ]],
							commit : function( data )
								{
									data.color1 = this.getValue();
								}
                         },
// OTHER PICTURE SETTINGS
                          {
								type : 'html',
                         html : ' <b>=====================================================</b></br><h1><strong> OTHER MAP PICTURE SETTINGS </strong></h1><b>=====================================================</b> '
							},
						{
								type : 'text',
								id : 'hor',
                          default : '512',
								label : 'Map Horizontal size in px (default=512 max=640)',
								validate : CKEDITOR.dialog.validate.notEmpty( 'The picture must have a horizontal size.' ),
								required : true,
								commit : function( data )
								{
									data.hor = this.getValue();
								}
							},
						{
								type : 'text',
								id : 'ver',
                          default : '512',
								label : 'Map vertical size in px (default=512 max=640)',
								validate : CKEDITOR.dialog.validate.notEmpty( 'The picture must have a vertical size.' ),
								required : true,
								commit : function( data )
								{
									data.ver= this.getValue();
								}
							},
							// Dialog window UI element: a selection field with link styles.
							// http://docs.cksource.com/ckeditor_api/symbols/CKEDITOR.ui.dialog.select.html
							{
								type : 'select',
								id : 'style',
								label : 'map type (default=map)',
								// Items that will appear inside the selection field, in pairs of displayed text and value.
								// http://docs.cksource.com/ckeditor_api/symbols/CKEDITOR.ui.dialog.select.html#constructor
								items : 
								[
									[ 'map', 'r' ],
									[ 'satellite', 's' ],
									[ 'hybrid', 'h' ]
								],
								commit : function( data )
								{
									data.style = this.getValue();
								}
							},

							{
								type : 'select',
								id : 'zoom',
						
								label : 'Zoom Map (default=12)',
								// Items that will appear inside the selection field, in pairs of displayed text and value.
								// http://docs.cksource.com/ckeditor_api/symbols/CKEDITOR.ui.dialog.select.html#constructor
								items : 
								[
									[ '<none>', '12' ],[ '0', '0' ],[ '1', '1' ], ['2', '2' ], [ '3', '3' ], [ '4', '4' ], [ '5', '5' ], [ '6', '6' ],
                             [ '7', '7' ], [ '8', '8' ], [ '9', '9' ], [ '10', '10' ], [ '11', '11' ], [ '12', '12' ], [ '13', '13' ], [ '14', '14' ],
                             [ '15', '15' ], [ '16', '16' ], [ '17', '17' ], [ '18', '18' ]
								],
								commit : function( data )
								{
									data.zoom = this.getValue();
								}
							},

		                 // Dialog window UI element: HTML code field.
							// http://docs.cksource.com/ckeditor_api/symbols/CKEDITOR.ui.dialog.html.html
							{
								type : 'html',
								// HTML code to be shown inside the field.
								// http://docs.cksource.com/ckeditor_api/symbols/CKEDITOR.ui.dialog.html.html#constructor
								html : 'If you have problems Email to zmajsoft@zmajsoft.com </br> <a href="www.zmajsoft.com" target="_blank">zmmaj</a> from zmajSoft-team'
							}
						]
					}
				],
		
				onOk : function()
				{
					// Create a link element and an object that will store the data entered in the dialog window.
					// http://docs.cksource.com/ckeditor_api/symbols/CKEDITOR.dom.document.html#createElement
					var dialog = this,
						data = {},
						link = editor.document.createElement( 'a' );
					// Populate the data object with data entered in the dialog window.
					// http://docs.cksource.com/ckeditor_api/symbols/CKEDITOR.dialog.html#commitContent
					this.commitContent( data );
    
					// Set the URL (href attribute) of the link element.
					// http://docs.cksource.com/ckeditor_api/symbols/CKEDITOR.dom.element.html#setAttribute
				//	link.setAttribute( 'href', data.url );
var tip="map"; 
	 switch( data.style )
					{
						case 'r' :
							tip='map';
						break;
						case 's' :
							tip='sat';
						break;
						case 'h' :
							tip='hyb';
						break;
					}

					// Insert the link element into the current cursor position in the editor.
					// http://docs.cksource.com/ckeditor_api/symbols/CKEDITOR.editor.html#insertElement ckeditor/plugins/OpenStreet/key.txt


	var kljuc=data.key;				
if (kljuc.length > 3){ 
var path = document.location.pathname;
var directory = path.substring(path.indexOf('/'), path.lastIndexOf('/'));
	var adr=directory +"/ckeditor/plugins/OpenStreet/save.php";
$.ajax({
	
  method: "POST",
  url: adr,
  data: { key: data.key}
})
} 	
if (data.lon1==0) {
                          editor.insertHtml('<img src="https://www.mapquestapi.com/staticmap/v4/getmap?size='+data.hor+','+data.ver+'&type=map&pois='+data.color0+','+data.lat+','+data.lon+'&zoom='+data.zoom+'&center='+data.lat+','+data.lon+'&imagetype=GIF&traffic=flow&key='+data.key+'" border="5" />' );
		}
if (data.lon1 !=0) {	

                          editor.insertHtml('<img src="https://www.mapquestapi.com/staticmap/v4/getmap?size='+data.hor+','+data.ver+'&type=map&pois='+data.color0+','+data.lat+','+data.lon+'|'+data.color1+','+data.lat1+','+data.lon1+'&zoom='+data.zoom+'&imagetype=GIF&traffic=flow&key='+data.key+'" border="5" />' );
			}
			

			
	}
			};
		} );
	}
} );



