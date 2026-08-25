import 'dart:js_interop';

@JS('gtag')
external void _gtag(JSAny? command, JSAny? eventName, JSAny? params);

void trackEvent(String name, [Map<String, Object?> params = const {}]) {
  _gtag('event'.toJS, name.toJS, params.jsify());
}
