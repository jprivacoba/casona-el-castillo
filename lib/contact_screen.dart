import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'theme.dart';

class ContactSection extends StatefulWidget {
  const ContactSection({super.key});

  @override
  State<ContactSection> createState() => _ContactSectionState();
}

class _ContactSectionState extends State<ContactSection> {
  final _formKey = GlobalKey<FormState>();
  final _nameController = TextEditingController();
  final _emailController = TextEditingController();
  final _messageController = TextEditingController();
  bool _isSent = false;
  bool _isLoading = false;

  @override
  void dispose() {
    _nameController.dispose();
    _emailController.dispose();
    _messageController.dispose();
    super.dispose();
  }

  Future<void> _submitForm() async {
    if (!_formKey.currentState!.validate()) return;
    setState(() => _isLoading = true);
    try {
      final isLocalhost = Uri.base.host == 'localhost' || Uri.base.host == '127.0.0.1';

      if (!isLocalhost) {
        final uri = Uri(
          scheme: Uri.base.scheme,
          host: Uri.base.host,
          port: Uri.base.port,
          path: '/',
        );
        final response = await http.post(
          uri,
          headers: {'Content-Type': 'application/x-www-form-urlencoded'},
          body: {
            'form-name': 'contacto',
            'nombre': _nameController.text,
            'correo': _emailController.text,
            'mensaje': _messageController.text,
          },
        );
        // Netlify devuelve 200 o redirige con 303
        if (response.statusCode >= 400) {
          throw Exception('Status ${response.statusCode}');
        }
      }

      setState(() {
        _isSent = true;
        _nameController.clear();
        _emailController.clear();
        _messageController.clear();
      });
    } catch (_) {
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(content: Text('Error al enviar. Intenta de nuevo.')),
        );
      }
    } finally {
      if (mounted) setState(() => _isLoading = false);
    }
  }

  @override
  Widget build(BuildContext context) {
    final isMobile = MediaQuery.of(context).size.width < 700;

    return Container(
      color: AppTheme.cream,
      padding: EdgeInsets.symmetric(
        vertical: isMobile ? 48 : 80,
        horizontal: isMobile ? 20 : 40,
      ),
      child: isMobile ? _buildMobile(context) : _buildDesktop(context),
    );
  }

  Widget _buildDesktop(BuildContext context) {
    return Row(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Expanded(
          flex: 2,
          child: Padding(
            padding: const EdgeInsets.only(right: 64, top: 8),
            child: _buildInfo(context),
          ),
        ),
        Expanded(
          flex: 3,
          child: _buildFormCard(),
        ),
      ],
    );
  }

  Widget _buildMobile(BuildContext context) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        _buildInfo(context),
        const SizedBox(height: 40),
        _buildFormCard(),
      ],
    );
  }

  Widget _buildInfo(BuildContext context) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        const Text(
          'CONTACTO',
          style: TextStyle(
            fontSize: 11,
            letterSpacing: 2.5,
            color: AppTheme.gold,
            fontWeight: FontWeight.w700,
          ),
        ),
        const SizedBox(height: 16),
        Text(
          'Coordinemos\ntu evento',
          style: Theme.of(context).textTheme.headlineMedium,
        ),
        const SizedBox(height: 8),
        Container(width: 48, height: 2, color: AppTheme.gold),
        const SizedBox(height: 28),
        const Text(
          'Escríbenos y te responderemos a la brevedad para organizar juntos el evento que imaginas.',
          style: TextStyle(
            fontSize: 14,
            color: AppTheme.muted,
            height: 1.8,
          ),
        ),
        const SizedBox(height: 40),
        _infoItem(Icons.phone_outlined, '+56 9 9779 4301'),
        const SizedBox(height: 16),
        _infoItem(Icons.email_outlined, 'casonaelcastillo1933@gmail.com'),
        const SizedBox(height: 16),
        _infoItem(Icons.location_on_outlined, 'Calle Larga, Los Andes\nValparaíso, Chile'),
      ],
    );
  }

  Widget _buildFormCard() {
    return Container(
      width: double.infinity,
      constraints: const BoxConstraints(maxWidth: 560),
      decoration: BoxDecoration(
        color: AppTheme.white,
        borderRadius: BorderRadius.circular(8),
        border: Border.all(color: const Color(0xFFE8DDD0)),
        boxShadow: const [
          BoxShadow(
            color: Color(0x0A000000),
            blurRadius: 24,
            offset: Offset(0, 8),
          ),
        ],
      ),
      padding: const EdgeInsets.all(32),
      child: _isSent ? _buildSuccess() : _buildForm(),
    );
  }

  Widget _buildSuccess() {
    return Column(
      mainAxisSize: MainAxisSize.min,
      children: [
        const SizedBox(height: 16),
        Container(
          width: 56,
          height: 56,
          decoration: BoxDecoration(
            color: AppTheme.gold.withValues(alpha: 0.12),
            shape: BoxShape.circle,
          ),
          child: const Icon(Icons.check, color: AppTheme.gold, size: 28),
        ),
        const SizedBox(height: 20),
        const Text(
          'Mensaje enviado',
          style: TextStyle(
            fontSize: 20,
            fontFamily: 'Playfair Display',
            fontWeight: FontWeight.w600,
            color: AppTheme.dark,
          ),
        ),
        const SizedBox(height: 10),
        const Text(
          'Gracias por contactarnos.\nTe responderemos a la brevedad.',
          textAlign: TextAlign.center,
          style: TextStyle(color: AppTheme.muted, fontSize: 14, height: 1.7),
        ),
        const SizedBox(height: 16),
      ],
    );
  }

  Widget _buildForm() {
    final isMobile = MediaQuery.of(context).size.width < 700;

    return Form(
      key: _formKey,
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        mainAxisSize: MainAxisSize.min,
        children: [
          const Text(
            'Envíanos un mensaje',
            style: TextStyle(
              fontSize: 18,
              fontFamily: 'Playfair Display',
              fontWeight: FontWeight.w600,
              color: AppTheme.dark,
            ),
          ),
          const SizedBox(height: 28),
          if (isMobile) ...[
            _field('Nombre', _nameController),
            const SizedBox(height: 16),
            _field('Correo electrónico', _emailController, isEmail: true),
          ] else
            Row(
              children: [
                Expanded(child: _field('Nombre', _nameController)),
                const SizedBox(width: 16),
                Expanded(child: _field('Correo electrónico', _emailController, isEmail: true)),
              ],
            ),
          const SizedBox(height: 20),
          _field('Mensaje', _messageController, isLong: true),
          const SizedBox(height: 28),
          SizedBox(
            width: double.infinity,
            child: ElevatedButton(
              onPressed: _isLoading ? null : _submitForm,
              child: _isLoading
                  ? const SizedBox(
                      height: 18,
                      width: 18,
                      child: CircularProgressIndicator(
                        strokeWidth: 2,
                        color: Colors.white,
                      ),
                    )
                  : const Text('ENVIAR SOLICITUD', style: TextStyle(letterSpacing: 1.5)),
            ),
          ),
        ],
      ),
    );
  }

  Widget _field(String label, TextEditingController controller,
      {bool isEmail = false, bool isLong = false}) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Text(
          label.toUpperCase(),
          style: const TextStyle(
            fontSize: 10,
            letterSpacing: 1.5,
            fontWeight: FontWeight.w700,
            color: AppTheme.muted,
          ),
        ),
        const SizedBox(height: 8),
        TextFormField(
          controller: controller,
          maxLines: isLong ? 5 : 1,
          style: const TextStyle(fontSize: 14, color: AppTheme.text),
          decoration: InputDecoration(
            filled: true,
            fillColor: AppTheme.cream,
            contentPadding: const EdgeInsets.symmetric(horizontal: 16, vertical: 14),
            border: OutlineInputBorder(
              borderRadius: BorderRadius.circular(4),
              borderSide: const BorderSide(color: Color(0xFFE0D5C5)),
            ),
            enabledBorder: OutlineInputBorder(
              borderRadius: BorderRadius.circular(4),
              borderSide: const BorderSide(color: Color(0xFFE0D5C5)),
            ),
            focusedBorder: OutlineInputBorder(
              borderRadius: BorderRadius.circular(4),
              borderSide: const BorderSide(color: AppTheme.gold, width: 1.5),
            ),
            errorBorder: OutlineInputBorder(
              borderRadius: BorderRadius.circular(4),
              borderSide: const BorderSide(color: Colors.redAccent),
            ),
          ),
          validator: (value) {
            if (value == null || value.isEmpty) return 'Campo requerido';
            if (isEmail && !value.contains('@')) return 'Correo inválido';
            return null;
          },
        ),
      ],
    );
  }

  Widget _infoItem(IconData icon, String text) {
    return Row(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Container(
          width: 36,
          height: 36,
          decoration: BoxDecoration(
            color: AppTheme.gold.withValues(alpha: 0.1),
            borderRadius: BorderRadius.circular(4),
          ),
          child: Icon(icon, color: AppTheme.gold, size: 18),
        ),
        const SizedBox(width: 14),
        Expanded(
          child: Padding(
            padding: const EdgeInsets.only(top: 8),
            child: Text(
              text,
              style: const TextStyle(fontSize: 13, color: AppTheme.text, height: 1.6),
            ),
          ),
        ),
      ],
    );
  }
}
