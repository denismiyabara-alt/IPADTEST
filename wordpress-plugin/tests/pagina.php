<?php
/**
 * Monta uma página de teste com um ou mais shortcodes, sem WordPress.
 * Imita as funções do WP que o plugin usa e imprime um HTML com o CSS e o JS enfileirados.
 *
 *   php tests/pagina.php <url-base-do-plugin> '[iec_ferramenta id="um-milhao" modo="compacto"]' ...
 */
define( 'ABSPATH', __DIR__ );
$GLOBALS['iec_teste'] = array( 'url' => rtrim( $argv[1], '/' ) . '/', 'css' => array(), 'js' => array(), 'sc' => array() );

function plugin_dir_path( $f ) { return dirname( $f ) . '/'; }
function plugin_dir_url( $f ) { return $GLOBALS['iec_teste']['url']; }
function sanitize_key( $k ) { return preg_replace( '/[^a-z0-9_\-]/', '', strtolower( (string) $k ) ); }
function wp_style_is( $h, $l ) { return true; }
function wp_register_style() {}
function wp_enqueue_style( $h, $src, $deps = array(), $ver = '' ) { $GLOBALS['iec_teste']['css'][ $h ] = $src . '?ver=' . $ver; }
function wp_enqueue_script( $h, $src, $deps = array(), $ver = '', $rodape = false ) { $GLOBALS['iec_teste']['js'][ $h ] = $src . '?ver=' . $ver; }
function add_action() {}
function add_shortcode( $tag, $fn ) { $GLOBALS['iec_teste']['sc'][ $tag ] = $fn; }
function esc_html( $s ) { return htmlspecialchars( (string) $s, ENT_QUOTES, 'UTF-8' ); }
function esc_attr( $s ) { return esc_html( $s ); }
function esc_url( $s ) { return preg_match( '#^(https?://|/)#', $s ) ? esc_html( $s ) : ''; }
function current_user_can( $c ) { return true; }
function shortcode_atts( $pares, $atts, $sc = '' ) {
	$out = array();
	foreach ( $pares as $k => $v ) { $out[ $k ] = array_key_exists( $k, $atts ) ? $atts[ $k ] : $v; }
	return $out;
}
/* Mesmo padrão do shortcode_parse_atts do WordPress (nomes em minúsculas). */
function shortcode_parse_atts( $texto ) {
	$atts = array();
	if ( preg_match_all( '/([\w-]+)\s*=\s*"([^"]*)"(?:\s|$)/', $texto, $m, PREG_SET_ORDER ) ) {
		foreach ( $m as $p ) { $atts[ strtolower( $p[1] ) ] = $p[2]; }
	}
	return $atts;
}

require dirname( __DIR__ ) . '/iec-ferramentas/iec-ferramentas.php';

$corpo = '';
foreach ( array_slice( $argv, 2 ) as $sc ) {
	if ( ! preg_match( '/^\[iec_ferramenta\s+(.*)\]$/s', trim( $sc ), $m ) ) {
		fwrite( STDERR, "shortcode inválido: $sc\n" );
		exit( 1 );
	}
	$corpo .= call_user_func( $GLOBALS['iec_teste']['sc']['iec_ferramenta'], shortcode_parse_atts( $m[1] ) ) . "\n";
}
echo "<!doctype html>\n<html lang=\"pt-BR\"><head><meta charset=\"utf-8\"><meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">\n<title>Teste iec-ferramentas</title>\n";
echo "<style>body{margin:0;padding:0 16px;background:#F7F8FA}</style>\n";
foreach ( $GLOBALS['iec_teste']['css'] as $h => $u ) { echo '<link rel="stylesheet" id="' . $h . '-css" href="' . $u . "\">\n"; }
echo "</head><body>\n" . $corpo;
foreach ( $GLOBALS['iec_teste']['js'] as $h => $u ) { echo '<script id="' . $h . '-js" src="' . $u . "\"></script>\n"; }
echo "</body></html>\n";
