<?php

define("BenchmarkForm_Name", "BenchmarkForm");
define("POST_IDENTIFIER", "submitDataForm");

if( !defined( 'MEDIAWIKI' ) ) die( "You can't run this directly." );

    // $wgExtensionCredits['validextensionclass'][] = array(
       // 'path' => __FILE__,
       // 'name' => 'BenchmarkExtension',
       // 'author' =>'Stattrav', 
       // 'url' => 'http://localhost/wiki/Extension:BenchmarkExtension', 
       // 'description' => 'Benchmark log submission API',
       // 'version'  => 0.1,
       // );
    $wgExtensionCredits['parserhook'][] = array(
         'name' => BenchmarkForm_Name,
         'version' => '0.8a',
         'author' =>'', 
         'url' => '',
         'description' => 'Inserts a form mailer into a page'
         );
 // Set up the new special page
$dir = dirname( __FILE__ ) . '/';

$wgExtensionMessagesFiles['BenchmarkExtension'] = $dir.'BenchmarkExtension.i18n.php';

// $wgAutoloadClasses['SpecialBenchmarkExtension'] = $dir.'SpecialBenchmarkExtension.php';
// $wgAutoloadClasses['BenchmarkPerformance'] = $dir.'BenchmarkExtension.hooks.php';

// $wgAutoloadClasses['ApiBenchmark'] = $dir.'BenchmarkExtension.api.php';
// $wgApiModules['benchmark'] = 'ApiBenchmark';


// $wgSpecialPages['BenchmarkExtension'] = 'SpecialBenchmarkExtension';
// $wgSpecialPageGroups['BenchmarkExtension'] = 'other';


$wgExtensionFunctions[] = 'benchmarkExtensionForms';


// $wgHooks['ParserFirstCallInit'][] = 'benchmarkExtensionForms';

function benchmarkExtensionForms(){
        
    global $wgParser;
    global $wgHooks;
    
    $wgParser->setHook( BenchmarkForm_Name, "renderBenchmarkForm" );
    
}


function renderBenchmarkForm($input, $argv, $parser){
    
    reset($_POST);
    $keys = array_keys($argv);
    
    // die(print_r($keys));
    $mode = strtolower(key($keys));             #This code eliminates an error related to referencing the $keys array by numerical keys

    ##############################
    ##### End of Custom Code #####
    ##############################

    #ORIGINAL# $mode = strtolower($keys[0]);    # See if first argument is 'form' or 'result'

    if ( $mode=='form' )    $argv = array_shift( $argv );    # Drop 'form' or 'result' for now
    else                    $mode = 'form';                    # Empty or a field type
 
    # Process form field(s)
    # Put this in a loop to allow multiple fields in one tag, 
    # e.g. <emailform name=60 email=60 comment=60x15 action=purge />
    $output = '';
    foreach ($argv as $arg => $value) {
        $output .= render_email_field($arg, $value, $ispost, $input, $parser, '');
    }
 
    # Render the outer tag as <form>input text<fields></form>
    if ( count($keys) != 1 )
        $output = render_email_field( $mode, '', $ispost, $input, $parser, $output );
    return( $output );
}

function render_email_field($arg, $value, $ispost, $input, &$parser, $extra) {
    global $wgTitle;
 
     switch ( strtolower($arg) ) {
 
    case 'result':    # Wrapper for results display
        if ( $ispost )
        {
            $parser->disableCache();     #### Important: Disable Cache ####
            return ( render_wikitext($parser, $input) );    # Show the results
        }
        return ( '' );        # Hide the results when showing the form 
 
    case 'form':    # Form wrapper
        # See if we're building the form
        if ( $ispost ) {
            # Get the remaining settings from [[MediaWiki:EmailForm]]
            $settings = get_MediaWikiEmailForm_settings ( $wgTitle->getText() );
            if ( $settings ) {
                 send_email($settings);        # Send the email message
                return ( '' );                # Hide the input form when showing results
            } else {
                return ( BenchmarkForm_Name . ': [[MediaWiki:' . BenchmarkForm_Name . ']] has no settings for [[' . $wgTitle->getText() . ']]' );
            }
        } else {
            if ( !($wgTitle->isProtected ('edit')) )
                return ( BenchmarkForm_Name . " is only active on protected pages." );
            $parser->disableCache();     #### Important: Disable Cache ####
            return (
                      '<form action="'. $wgTitle->getFullURL() . '" method="post">'
                    . '<input type="hidden" name="action" value="purge" />'
                    . '<input type="hidden" name="' . POST_IDENTIFIER . '" value="send" />'
                    . render_wikitext($parser, $input) . $extra
                    . '</form>' 
            );
        }
 
    case 'submit':        return( ' <input type="submit" name="submit" value="' . $value . '"/> ' );
 
    default:
        # Result: Display contents of corresponding field
        if ($ispost)     return( $_POST[$arg] );
        # Build other form fields
        # If the argument is numeric, it's a text field size
        if ( $value > 0 ) {
            $size = explode( 'x', $value );
 
            #######################
            ##### Custom Code #####
            #######################

                if(count($size)>1) {    #This code eliminates an error related to referencing the $size array by numerical keys
                        reset($size);
                        $firstpiece = ('<textarea name="'.$arg.'" cols="'.current($size).'"');
                        next($size);
                        $secondpiece = (' rows="'.current($size).'" ></textarea>' );
                        return($firstpiece.$secondpiece);
                }
 
            ##############################
            ##### End of Custom Code #####
            ##############################

            #ORIGINAL# if ( $size[1] ) return( '<textarea name="'.$arg.'" cols="'.$size[0].'" rows="'.$size[1].'" ></textarea>' );
            else            return( '<input type="text" name="'. $arg.'" size="'.$value.'" />' );
        }
 
        # Arbitrary hidden fields
        return( '<input type="hidden" name="'.$arg.'" value="'.$value.'" />' );
    }
}

function submitDataForm($settings){
    
    return true;
}

?>