import 'dart:convert';
import 'dart:io';

import 'package:lvc_gui_flutter/constantsx.dart';
import 'package:lvc_gui_flutter/main.dart';

Future<void> launch() async {
  Process process = await Process.start('linux-voice-control', ['--ui=true']);
  process.stderr.transform(utf8.decoder).forEach((line) {
    if (line.contains('listening')) {
      setTag(ConstantsX.listeningTag);
      setStatus('linux-voice-control');
    } else if (line.startsWith("saving audio")) {
      setTag(ConstantsX.computingTag);
      setStatus('thinking');
    } else if (line.contains("probability:")) {
      try {
        int percentage = int.parse(line
            .substring(line.lastIndexOf(',') + 1, line.length - 2)
            .trim());
        if (percentage > 60) {
          setTag(ConstantsX.executingTag);
          setStatus("found a perfect match");
        } else {
          setStatus("no match found");
        }
      } catch (e) {
        print(e);
      }
    } else if (line == "no voice") {
      setStatus("empty clip");
    } else if (line == "no speech in clip") {
      setStatus("no voice in clip");
    }
  }).whenComplete(() => exit(0));
}
