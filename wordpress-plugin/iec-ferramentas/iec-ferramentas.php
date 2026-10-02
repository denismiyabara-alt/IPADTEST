<?php
/**
 * Plugin Name:       IEC Ferramentas
 * Description:       Calculadoras e simuladores do Investir e Coçar. Use o shortcode [iec_ferramenta id="..."], por exemplo [iec_ferramenta id="simulador-ntnb"].
 * Version:           1.2.0
 * Requires at least: 5.6
 * Requires PHP:      7.4
 * Author:            Investir e Coçar
 * License:           GPL-2.0-or-later
 * Text Domain:       iec-ferramentas
 */

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

define( 'IEC_FERRAMENTAS_DIR', plugin_dir_path( __FILE__ ) . 'ferramentas/' );
define( 'IEC_FERRAMENTAS_URL', plugin_dir_url( __FILE__ ) . 'ferramentas/' );
define( 'IEC_FERRAMENTAS_FONTES', 'https://fonts.googleapis.com/css2?family=Archivo:wght@400;600;700;800&family=IBM+Plex+Sans:wght@400;500;600;700&display=swap' );

/**
 * Valida o id e devolve a pasta da ferramenta, ou null se ela não existir.
 */
function iec_ferramentas_pasta( $id ) {
	$id = sanitize_key( $id );
	if ( '' === $id ) {
		return null;
	}
	$pasta = IEC_FERRAMENTAS_DIR . $id . '/';
	return is_readable( $pasta . 'markup.html' ) ? $pasta : null;
}

/**
 * Enfileira CSS e JS de uma ferramenta. Versão = data de modificação do arquivo,
 * então qualquer atualização fura o cache do navegador e do WP-Optimize.
 */
function iec_ferramentas_enfileirar( $id ) {
	$id    = sanitize_key( $id );
	$pasta = iec_ferramentas_pasta( $id );
	if ( null === $pasta ) {
		return;
	}
	$handle = 'iec-ferramenta-' . $id;
	$url    = IEC_FERRAMENTAS_URL . $id . '/';

	if ( ! wp_style_is( 'iec-ferramentas-fontes', 'registered' ) ) {
		wp_register_style( 'iec-ferramentas-fontes', IEC_FERRAMENTAS_FONTES, array(), null );
	}
	if ( is_readable( $pasta . 'style.css' ) ) {
		wp_enqueue_style( $handle, $url . 'style.css', array( 'iec-ferramentas-fontes' ), (string) filemtime( $pasta . 'style.css' ) );
	}
	if ( is_readable( $pasta . 'app.js' ) ) {
		wp_enqueue_script( $handle, $url . 'app.js', array(), (string) filemtime( $pasta . 'app.js' ), true );
	}
}

/**
 * Lista os ids usados no conteúdo de um post.
 */
function iec_ferramentas_ids_no_conteudo( $conteudo ) {
	$ids = array();
	if ( false === strpos( $conteudo, '[iec_ferramenta' ) ) {
		return $ids;
	}
	if ( preg_match_all( '/' . get_shortcode_regex( array( 'iec_ferramenta' ) ) . '/', $conteudo, $m, PREG_SET_ORDER ) ) {
		foreach ( $m as $sc ) {
			$atts = shortcode_parse_atts( $sc[3] );
			if ( is_array( $atts ) && ! empty( $atts['id'] ) ) {
				$ids[] = sanitize_key( $atts['id'] );
			}
		}
	}
	return array_unique( $ids );
}

/**
 * Carrega o CSS no <head> só nas páginas que usam o shortcode (evita o "pisca" sem estilo).
 */
function iec_ferramentas_wp_enqueue_scripts() {
	if ( ! is_singular() ) {
		return;
	}
	$post = get_queried_object();
	if ( ! $post instanceof WP_Post ) {
		return;
	}
	foreach ( iec_ferramentas_ids_no_conteudo( $post->post_content ) as $id ) {
		iec_ferramentas_enfileirar( $id );
	}
}
add_action( 'wp_enqueue_scripts', 'iec_ferramentas_wp_enqueue_scripts' );

/**
 * [iec_ferramenta id="simulador-ntnb"]
 * Devolve só o HTML. CSS e JS vão por wp_enqueue_*, fora do the_content.
 */
function iec_ferramentas_shortcode( $atts ) {
	$atts  = shortcode_atts( array( 'id' => '' ), $atts, 'iec_ferramenta' );
	$id    = sanitize_key( $atts['id'] );
	$pasta = iec_ferramentas_pasta( $id );

	if ( null === $pasta ) {
		if ( current_user_can( 'edit_posts' ) ) {
			return '<p><strong>[iec_ferramenta]</strong> Ferramenta "' . esc_html( $id ) . '" não encontrada em wp-content/plugins/iec-ferramentas/ferramentas/.</p>';
		}
		return '';
	}

	/* Garantia para quando o shortcode vem de widget, template ou bloco reutilizável. */
	iec_ferramentas_enfileirar( $id );

	$markup = file_get_contents( $pasta . 'markup.html' );
	return false === $markup ? '' : $markup;
}
add_shortcode( 'iec_ferramenta', 'iec_ferramentas_shortcode' );
