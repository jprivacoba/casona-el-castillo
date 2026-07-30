import 'package:flutter/material.dart';
import 'theme.dart';

/// Sección de preguntas frecuentes.
///
/// IMPORTANTE (SEO): estas preguntas y respuestas deben coincidir LITERALMENTE
/// con el FAQPage del JSON-LD y con los <dt>/<dd> del espejo SEO, ambos en
/// `web/index.html`. Google exige que las preguntas del structured data estén
/// visibles en la página; por eso esta sección existe.
///
/// Si editas una pregunta acá, actualiza también `web/index.html` (JSON-LD +
/// #seo-content) y `web/llms.txt`, y corre `python3 tool/validar_seo.py`.
const List<({String pregunta, String respuesta})> kFaqItems = [
  (
    pregunta: '¿Cuál es la capacidad máxima de invitados?',
    respuesta:
        'La carpa de eventos es un espacio adaptable para más de 300 personas. '
        'El parque centenario permite distribuir la ceremonia, el cóctel y la '
        'recepción en distintos sectores del recinto.',
  ),
  (
    pregunta: '¿Se puede llevar un proveedor externo de catering o banquetería?',
    respuesta:
        'Sí. Puedes traer tu propio proveedor de banquetería. La casona cuenta '
        'con una cocina de más de 300 m² restaurada, que queda disponible para '
        'el equipo de catering que elijas.',
  ),
  (
    pregunta: '¿Hay estacionamiento para los invitados?',
    respuesta:
        'Sí. El recinto cuenta con estacionamiento privado dentro del terreno '
        'para los invitados, con acceso privado al parque.',
  ),
  (
    pregunta: '¿Se puede realizar la ceremonia civil en el lugar?',
    respuesta:
        'Sí. La ceremonia civil se puede realizar en el mismo recinto, en los '
        'jardines del parque centenario, de modo que la ceremonia y la '
        'celebración ocurran en un solo lugar.',
  ),
  (
    pregunta: '¿Qué pasa si llueve el día del evento?',
    respuesta:
        'El evento se traslada a la carpa de eventos, que tiene clima '
        'controlado, iluminación especial y equipamiento completo para más de '
        '300 personas. Así la celebración se realiza igual, sin depender del '
        'clima.',
  ),
  (
    pregunta: '¿Cómo reservo una fecha o agendo una visita al lugar?',
    respuesta:
        'Escríbenos por WhatsApp al +56 9 9779 4301, al correo '
        'casonaelcastillo1933@gmail.com, o completa el formulario de contacto '
        'del sitio indicando fecha, número de invitados y el estilo de evento '
        'que imaginas. Te responderemos a la brevedad para coordinar una visita '
        'al recinto.',
  ),
  (
    pregunta: '¿Dónde queda Casona Fundo El Castillo y cómo llego?',
    respuesta:
        'Está en Calle Larga, provincia de Los Andes, Región de Valparaíso, a 5 '
        'minutos del Casino Enjoy Santiago y a unos 75 km de Santiago, con '
        'acceso fácil en auto.',
  ),
  (
    pregunta: '¿Qué tipos de evento se realizan en la Casona?',
    respuesta:
        'Matrimonios y ceremonias íntimas o grandes, eventos corporativos, '
        'reuniones y celebraciones, fiestas y cumpleaños, y sesiones de '
        'fotografía y producciones audiovisuales que aprovechan los escenarios '
        'del parque.',
  ),
  (
    pregunta: '¿Cuánto cuesta arrendar el lugar para un matrimonio?',
    respuesta:
        'El valor se cotiza caso a caso según la fecha, el número de invitados '
        'y los servicios que incluyas. Escríbenos por WhatsApp al '
        '+56 9 9779 4301 o al correo casonaelcastillo1933@gmail.com y te '
        'enviamos una cotización.',
  ),
];

class FaqSection extends StatelessWidget {
  const FaqSection({super.key});

  @override
  Widget build(BuildContext context) {
    final isMobile = MediaQuery.of(context).size.width < 700;

    return Container(
      color: AppTheme.creamAlt,
      padding: EdgeInsets.symmetric(
        vertical: isMobile ? 48 : 72,
        horizontal: isMobile ? 20 : 40,
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            children: [
              Container(width: 32, height: 1.5, color: AppTheme.gold),
              const SizedBox(width: 10),
              const Text(
                'PREGUNTAS FRECUENTES',
                style: TextStyle(
                  fontSize: 11,
                  letterSpacing: 2.5,
                  color: AppTheme.gold,
                  fontWeight: FontWeight.w700,
                ),
              ),
            ],
          ),
          const SizedBox(height: 14),
          Text(
            'Lo que suelen preguntarnos',
            style: Theme.of(context).textTheme.headlineMedium,
          ),
          const SizedBox(height: 6),
          Container(width: 48, height: 2, color: AppTheme.gold),
          const SizedBox(height: 8),
          const Text(
            'Si tu duda no está aquí, escríbenos y la resolvemos.',
            style: TextStyle(color: AppTheme.muted, fontSize: 13, height: 1.6),
          ),
          const SizedBox(height: 28),
          Center(
            child: ConstrainedBox(
              constraints: const BoxConstraints(maxWidth: 820),
              child: Column(
                children: [
                  for (final item in kFaqItems)
                    _FaqTile(
                      pregunta: item.pregunta,
                      respuesta: item.respuesta,
                      isMobile: isMobile,
                    ),
                ],
              ),
            ),
          ),
        ],
      ),
    );
  }
}

class _FaqTile extends StatefulWidget {
  final String pregunta;
  final String respuesta;
  final bool isMobile;

  const _FaqTile({
    required this.pregunta,
    required this.respuesta,
    required this.isMobile,
  });

  @override
  State<_FaqTile> createState() => _FaqTileState();
}

class _FaqTileState extends State<_FaqTile> {
  bool _expanded = false;

  @override
  Widget build(BuildContext context) {
    return Container(
      margin: const EdgeInsets.only(bottom: 10),
      decoration: BoxDecoration(
        color: AppTheme.white,
        borderRadius: BorderRadius.circular(6),
        border: Border.all(
          color: _expanded ? AppTheme.gold : const Color(0xFFE0D5C5),
        ),
      ),
      clipBehavior: Clip.antiAlias,
      child: Theme(
        // Quita las líneas divisorias propias del ExpansionTile: el borde del
        // Container ya delimita cada pregunta.
        data: Theme.of(context).copyWith(dividerColor: Colors.transparent),
        child: ExpansionTile(
          onExpansionChanged: (v) => setState(() => _expanded = v),
          tilePadding: EdgeInsets.symmetric(
            horizontal: widget.isMobile ? 16 : 24,
            vertical: 4,
          ),
          childrenPadding: EdgeInsets.only(
            left: widget.isMobile ? 16 : 24,
            right: widget.isMobile ? 16 : 24,
            bottom: 20,
          ),
          expandedCrossAxisAlignment: CrossAxisAlignment.start,
          iconColor: AppTheme.gold,
          collapsedIconColor: AppTheme.muted,
          shape: const Border(),
          collapsedShape: const Border(),
          title: Text(
            widget.pregunta,
            style: TextStyle(
              fontSize: widget.isMobile ? 14 : 15,
              fontWeight: FontWeight.w600,
              color: AppTheme.text,
              height: 1.5,
            ),
          ),
          children: [
            Text(
              widget.respuesta,
              style: const TextStyle(
                fontSize: 14,
                color: AppTheme.muted,
                height: 1.75,
              ),
            ),
          ],
        ),
      ),
    );
  }
}
