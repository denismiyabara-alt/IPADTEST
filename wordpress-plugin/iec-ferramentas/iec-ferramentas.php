<?php
/**
 * Plugin Name:       IEC Ferramentas
 * Description:       Calculadoras e simuladores do Investir e Coçar. Use o shortcode [iec_ferramenta id="..."], por exemplo [iec_ferramenta id="simulador-ntnb"].
 * Version:           1.3.1
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
 * Preenche campos da ferramenta com atributos do shortcode.
 * Cada atributo extra cujo nome é o id de um <input> do markup troca o value desse campo.
 * Só aceita número (ex.: 1500 ou 6,5) ou data (AAAA-MM-DD); qualquer outra coisa é ignorada.
 */
function iec_ferramentas_preencher( $markup, $atts ) {
	foreach ( $atts as $campo => $valor ) {
		if ( ! is_string( $campo ) || in_array( $campo, array( 'id', 'modo', 'metodologia' ), true ) ) {
			continue;
		}
		if ( ! preg_match( '/^[a-z0-9][a-z0-9_-]*$/', $campo ) ) {
			continue;
		}
		$valor = trim( (string) $valor );
		if ( preg_match( '/^-?\d+(?:[.,]\d+)?$/', $valor ) ) {
			$valor = str_replace( ',', '.', $valor );
		} elseif ( ! preg_match( '/^\d{4}-\d{2}-\d{2}$/', $valor ) ) {
			continue;
		}
		$markup = preg_replace(
			'/(<input id="' . preg_quote( $campo, '/' ) . '"[^>]*?\svalue=")[^"]*(")/',
			'${1}' . $valor . '${2}',
			$markup,
			1
		);
	}
	return $markup;
}

/**
 * modo="compacto": tira a seção explicativa (<section class="explain">) e põe uma linha
 * com o aviso educativo e, se houver, o link para a metodologia. Serve para páginas que
 * repetem a mesma ferramenta muitas vezes (ex.: uma página por ativo).
 */
function iec_ferramentas_compactar( $markup, $metodologia ) {
	$linha = 'Ferramenta educativa, não é recomendação de investimento.';
	if ( '' !== $metodologia ) {
		$linha .= ' <a href="' . esc_url( $metodologia ) . '">Veja as premissas e a metodologia</a>.';
	}
	$markup = preg_replace_callback(
		'/\s*<section class="explain">.*?<\/section>/s',
		function () use ( $linha ) {
			return "\n  <p class=\"iec-compacto\">" . $linha . '</p>';
		},
		$markup,
		1
	);
	return preg_replace(
		'/<div id="([a-z0-9_-]+)" class="iec-ferramenta"/',
		'<div id="$1" class="iec-ferramenta" data-modo="compacto"',
		$markup,
		1
	);
}

/**
 * [iec_ferramenta id="simulador-ntnb"]
 * Opcional: modo="compacto", metodologia="/link/" e um atributo por campo a preencher,
 * ex.: [iec_ferramenta id="um-milhao" um-aporte="1500" um-taxa="5" modo="compacto"].
 * Devolve só o HTML. CSS e JS vão por wp_enqueue_*, fora do the_content.
 */
function iec_ferramentas_shortcode( $atts ) {
	$brutos = is_array( $atts ) ? $atts : array();
	$atts   = shortcode_atts( array( 'id' => '', 'modo' => '', 'metodologia' => '' ), $brutos, 'iec_ferramenta' );
	$id     = sanitize_key( $atts['id'] );
	$pasta  = iec_ferramentas_pasta( $id );

	if ( null === $pasta ) {
		if ( current_user_can( 'edit_posts' ) ) {
			return '<p><strong>[iec_ferramenta]</strong> Ferramenta "' . esc_html( $id ) . '" não encontrada em wp-content/plugins/iec-ferramentas/ferramentas/.</p>';
		}
		return '';
	}

	/* Garantia para quando o shortcode vem de widget, template ou bloco reutilizável. */
	iec_ferramentas_enfileirar( $id );

	$markup = file_get_contents( $pasta . 'markup.html' );
	if ( false === $markup ) {
		return '';
	}
	$markup = iec_ferramentas_preencher( $markup, $brutos );
	if ( 'compacto' === $atts['modo'] ) {
		$markup = iec_ferramentas_compactar( $markup, trim( (string) $atts['metodologia'] ) );
	}
	return $markup;
}
add_shortcode( 'iec_ferramenta', 'iec_ferramentas_shortcode' );
