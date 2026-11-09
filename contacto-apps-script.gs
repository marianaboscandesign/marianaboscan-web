// Formularios de marianaboscan.com
// 1) Contacto: guarda en la hoja "Mensajes", te avisa y confirma a quien escribió.
// 2) Briefs por servicio: guarda en la hoja "Briefs", te manda las respuestas ordenadas y confirma al cliente.

function libro() {
  var ss = SpreadsheetApp.getActiveSpreadsheet();
  if (!ss) {
    var p = PropertiesService.getScriptProperties();
    var id = p.getProperty('SHEET_ID');
    if (id) { try { ss = SpreadsheetApp.openById(id); } catch (e) { ss = null; } }
    if (!ss) { ss = SpreadsheetApp.create('Contactos web - Mariana Boscán'); p.setProperty('SHEET_ID', ss.getId()); }
  }
  return ss;
}

function hoja() {
  var ss = libro();
  var h = ss.getSheetByName('Mensajes');
  if (!h) {
    h = ss.insertSheet('Mensajes');
    h.appendRow(['Fecha', 'Nombre', 'Email', 'Teléfono', 'Cómo me conoció', 'Mensaje', 'Idioma']);
    h.setFrozenRows(1);
  }
  return h;
}

function hojaBriefs() {
  var ss = libro();
  var h = ss.getSheetByName('Briefs');
  if (!h) {
    h = ss.insertSheet('Briefs');
    h.appendRow(['Fecha', 'Servicio', 'Nombre', 'Email', 'Teléfono', 'Idioma', 'Respuestas']);
    h.setFrozenRows(1);
  }
  return h;
}

function doPost(e) {
  try {
    var d = JSON.parse(e.postData.contents);
    if (d.web) return salida({ ok: true });
    if (d.formulario === 'brief') return recibirBrief(d);
    var en = d.idioma === 'en';
    var nombre = String(d.nombre || '').trim().slice(0, 120);
    var email = String(d.email || '').trim().slice(0, 200);
    var tel = String(d.telefono || '').trim().slice(0, 40);
    var origen = String(d.origen_texto || '').trim().slice(0, 80);
    if (!d.origen) origen = '';
    var mensaje = String(d.mensaje || '').trim().slice(0, 4000);
    if (!nombre || !mensaje || !/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(email)) return salida({ ok: false, error: 'datos_invalidos' });

    var h = hoja();
    var desde = Date.now() - 24 * 3600 * 1000;
    var filas = h.getDataRange().getValues().slice(1).filter(function (f) { return new Date(f[0]).getTime() > desde; });
    if (filas.length >= 40 || filas.filter(function (f) { return String(f[2]).toLowerCase() === email.toLowerCase(); }).length >= 3) {
      return salida({ ok: false, error: 'limite' });
    }
    h.appendRow([new Date(), seguro(nombre), seguro(email), seguro(tel), seguro(origen), seguro(mensaje), en ? 'en' : 'es']);

    // 1) Aviso para ti
    MailApp.sendEmail({
      to: Session.getEffectiveUser().getEmail(),
      replyTo: email,
      subject: 'Nuevo mensaje desde tu web: ' + nombre,
      body: 'De: ' + nombre + ' <' + email + '>\n' +
            'Teléfono: ' + (tel || '—') + '\n' +
            'Cómo te conoció: ' + (origen || '—') + '\n' +
            'Idioma: ' + (en ? 'English' : 'Español') + '\n\n' + mensaje,
      name: 'Web Mariana Boscán'
    });

    // 2) Confirmación para quien escribió (si falla, el mensaje ya quedó guardado)
    try { confirmar(nombre, email, mensaje, en); } catch (err) {}

    return salida({ ok: true });
  } catch (err) {
    return salida({ ok: false, error: 'solicitud_invalida', detalle: String(err) });
  }
}

function confirmar(nombre, email, mensaje, en) {
  var primer = nombre.split(' ')[0];
  var T = en
    ? { asunto: 'I got your message, ' + primer, hola: 'Hi ' + primer + ',',
        p1: 'Thank you for writing to me. I received your message and I’ll reply to you soon.',
        tu: 'Your message', firma: 'Mariana Boscán', rol: 'Graphic designer',
        nota: 'If you didn’t send this message, you can ignore this email.' }
    : { asunto: 'Recibí tu mensaje, ' + primer, hola: 'Hola ' + primer + ',',
        p1: 'Gracias por escribirme. Recibí tu mensaje y te respondo pronto.',
        tu: 'Tu mensaje', firma: 'Mariana Boscán', rol: 'Diseñadora gráfica',
        nota: 'Si no fuiste tú quien envió este mensaje, puedes ignorar este correo.' };
  var html =
    '<div style="background:#ebecf9;padding:24px 12px;font-family:Arial,Helvetica,sans-serif;">' +
    '<div style="max-width:560px;margin:0 auto;background:#ffffff;border-radius:24px;overflow:hidden;">' +
    '<div style="background:#14141e;padding:18px 24px;color:#ffffff;font-size:15px;font-weight:700;">mariana boscán</div>' +
    '<div style="padding:28px 24px 8px;color:#14141e;font-size:16px;line-height:1.55;">' +
    '<p style="margin:0 0 12px;font-family:Georgia,serif;font-size:26px;line-height:1.2;">' + esc(T.hola) + '</p>' +
    '<p style="margin:0 0 20px;">' + esc(T.p1) + '</p>' +
    '<div style="background:#ebecf9;border-radius:16px;padding:16px 18px;">' +
    '<div style="font-size:13px;font-weight:700;color:#5a5a62;margin-bottom:6px;">' + esc(T.tu) + '</div>' +
    '<div style="font-size:15px;color:#14141e;white-space:pre-wrap;">' + esc(mensaje) + '</div></div>' +
    '<p style="margin:22px 0 0;">' + esc(T.firma) + '<br><span style="color:#5a5a62;">' + esc(T.rol) + '</span></p></div>' +
    '<div style="padding:16px 24px 24px;font-size:12px;line-height:1.5;color:#5a5a62;">' + esc(T.nota) + '<br>' +
    '<a href="https://www.marianaboscan.com" style="color:#5a5a62;">marianaboscan.com</a></div>' +
    '</div></div>';
  MailApp.sendEmail({
    to: email,
    replyTo: Session.getEffectiveUser().getEmail(),
    subject: T.asunto,
    body: T.hola + '\n\n' + T.p1 + '\n\n' + T.tu + ':\n' + mensaje + '\n\n' + T.firma + '\n' + T.rol + '\nhttps://www.marianaboscan.com\n\n' + T.nota,
    htmlBody: html,
    name: 'Mariana Boscán'
  });
}

function esc(s) {
  return String(s == null ? '' : s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
}
function doGet() { return salida({ ok: true, servicio: 'formularios' }); }
function salida(o) { return ContentService.createTextOutput(JSON.stringify(o)).setMimeType(ContentService.MimeType.JSON); }
function seguro(s) { s = String(s == null ? '' : s); return /^[=+\-@]/.test(s) ? "'" + s : s; }

// ---------- Briefs ----------
function recibirBrief(d) {
  var en = d.idioma === 'en';
  var servicio = String(d.servicio || '').trim().slice(0, 120);
  var nombre = String(d.nombre || '').trim().slice(0, 120);
  var email = String(d.email || '').trim().slice(0, 200);
  var tel = String(d.telefono || '').trim().slice(0, 40);
  var resp = (d.respuestas && d.respuestas.length) ? d.respuestas.slice(0, 60) : [];
  resp = resp.map(function (x) { return { p: String(x.p || '').slice(0, 200), r: String(x.r || '').slice(0, 3000) }; })
             .filter(function (x) { return x.p && x.r; });
  if (!nombre || !servicio || !resp.length || !/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(email)) return salida({ ok: false, error: 'datos_invalidos' });

  var h = hojaBriefs();
  var desde = Date.now() - 24 * 3600 * 1000;
  var filas = h.getDataRange().getValues().slice(1).filter(function (f) { return new Date(f[0]).getTime() > desde; });
  if (filas.length >= 30 || filas.filter(function (f) { return String(f[3]).toLowerCase() === email.toLowerCase(); }).length >= 3) {
    return salida({ ok: false, error: 'limite' });
  }
  var texto = resp.map(function (x) { return x.p + ': ' + x.r; }).join('\n');
  h.appendRow([new Date(), seguro(servicio), seguro(nombre), seguro(email), seguro(tel), en ? 'en' : 'es', seguro(texto)]);

  // 1) Aviso para ti, con las respuestas ordenadas
  MailApp.sendEmail({
    to: Session.getEffectiveUser().getEmail(),
    replyTo: email,
    subject: 'Nuevo brief: ' + servicio + ' — ' + nombre,
    body: servicio + '\n' + nombre + ' <' + email + '>\nIdioma: ' + (en ? 'English' : 'Español') + '\n\n' + texto,
    htmlBody: '<div style="font-family:Arial,Helvetica,sans-serif;max-width:640px;color:#14141e;">' +
      '<h2 style="margin:0 0 4px;">' + esc(servicio) + '</h2>' +
      '<p style="margin:0 0 16px;color:#5a5a62;">' + esc(nombre) + ' · <a href="mailto:' + esc(email) + '">' + esc(email) + '</a> · ' + (en ? 'English' : 'Español') + '</p>' +
      tablaRespuestas(resp) + '</div>',
    name: 'Web Mariana Boscán'
  });

  // 2) Confirmación para el cliente (si falla, el brief ya quedó guardado)
  try { confirmarBrief(nombre, email, servicio, resp, en); } catch (err) {}
  return salida({ ok: true });
}

function tablaRespuestas(resp) {
  return '<table style="width:100%;border-collapse:collapse;font-size:14px;line-height:1.5;">' + resp.map(function (x) {
    return '<tr><td style="padding:10px 12px;border-bottom:1px solid #e3e3e4;vertical-align:top;width:38%;font-weight:700;color:#5a5a62;">' + esc(x.p) +
           '</td><td style="padding:10px 12px;border-bottom:1px solid #e3e3e4;vertical-align:top;white-space:pre-wrap;">' + esc(x.r) + '</td></tr>';
  }).join('') + '</table>';
}

function confirmarBrief(nombre, email, servicio, resp, en) {
  var primer = nombre.split(' ')[0];
  var T = en
    ? { asunto: 'I got your brief, ' + primer, hola: 'Hi ' + primer + ',',
        p1: 'Thank you for filling in the brief (' + servicio + '). I received it and I’ll review it carefully. I’ll write to you soon with the next steps.',
        tu: 'Your answers', firma: 'Mariana Boscán', rol: 'Graphic designer',
        nota: 'If you didn’t send this brief, you can ignore this email.' }
    : { asunto: 'Recibí tu brief, ' + primer, hola: 'Hola ' + primer + ',',
        p1: 'Gracias por llenar el brief (' + servicio + '). Lo recibí y lo voy a revisar con calma. Te escribo pronto con los siguientes pasos.',
        tu: 'Tus respuestas', firma: 'Mariana Boscán', rol: 'Diseñadora gráfica',
        nota: 'Si no fuiste tú quien envió este brief, puedes ignorar este correo.' };
  var html =
    '<div style="background:#ebecf9;padding:24px 12px;font-family:Arial,Helvetica,sans-serif;">' +
    '<div style="max-width:600px;margin:0 auto;background:#ffffff;border-radius:24px;overflow:hidden;">' +
    '<div style="background:#14141e;padding:18px 24px;color:#ffffff;font-size:15px;font-weight:700;">mariana boscán</div>' +
    '<div style="padding:28px 24px 8px;color:#14141e;font-size:16px;line-height:1.55;">' +
    '<p style="margin:0 0 12px;font-family:Georgia,serif;font-size:26px;line-height:1.2;">' + esc(T.hola) + '</p>' +
    '<p style="margin:0 0 20px;">' + esc(T.p1) + '</p>' +
    '<div style="background:#ebecf9;border-radius:16px;padding:8px 6px;">' +
    '<div style="font-size:13px;font-weight:700;color:#5a5a62;margin:8px 12px 2px;">' + esc(T.tu) + '</div>' + tablaRespuestas(resp) + '</div>' +
    '<p style="margin:22px 0 0;">' + esc(T.firma) + '<br><span style="color:#5a5a62;">' + esc(T.rol) + '</span></p></div>' +
    '<div style="padding:16px 24px 24px;font-size:12px;line-height:1.5;color:#5a5a62;">' + esc(T.nota) + '<br>' +
    '<a href="https://www.marianaboscan.com" style="color:#5a5a62;">marianaboscan.com</a></div>' +
    '</div></div>';
  MailApp.sendEmail({
    to: email,
    replyTo: Session.getEffectiveUser().getEmail(),
    subject: T.asunto,
    body: T.hola + '\n\n' + T.p1 + '\n\n' + T.tu + ':\n' + resp.map(function (x) { return x.p + ': ' + x.r; }).join('\n') + '\n\n' + T.firma + '\n' + T.rol + '\nhttps://www.marianaboscan.com\n\n' + T.nota,
    htmlBody: html,
    name: 'Mariana Boscán'
  });
}

// Ejecútala UNA vez a mano: crea la hoja "Mensajes" y te manda un correo de prueba de la confirmación.
function probar() {
  hoja();
  hojaBriefs();
  confirmar('Prueba Demo', Session.getEffectiveUser().getEmail(), 'Este es un mensaje de prueba.', false);
}
