import 'package:bitsdojo_window/bitsdojo_window.dart';
import 'package:flutter/material.dart';
import 'package:lvc_gui_flutter/constantsx.dart';
import 'package:lvc_gui_flutter/lvc_handler.dart';
import 'package:lvc_gui_flutter/themex.dart';
import 'package:lvc_gui_flutter/ui/home_screen.dart';


GlobalKey<HomeScreenState> homeScreenKey = GlobalKey();

Future<void> main() async {
  runApp(const App());

  doWhenWindowReady(() {
    const initialSize = Size(180, 100);
    appWindow.minSize = initialSize;
    appWindow.size = initialSize;
    appWindow.alignment = Alignment.center;
    appWindow.show();
  });

  await launch();
}

var tag = ConstantsX.initializingTag;
var status = "linux-voice-control";

void setTag(int newTag){
  tag = newTag;
  homeScreenKey.currentState?.rebuild();
}

void setStatus(String newStatus){
  status = newStatus;
  homeScreenKey.currentState?.rebuild();
}

Color inferTagColor(){
  if(tag == ConstantsX.initializingTag) {
    return ThemeX.initializingColor;
  }
  else if(tag == ConstantsX.listeningTag) {
    return ThemeX.listeningColor;
  }
  else if(tag == ConstantsX.computingTag) {
    return ThemeX.computingColor;
  }
  return ThemeX.executingColor;
}

String inferTagText(){
  if(tag == ConstantsX.initializingTag) {
    return "initializing...";
  }
  else if(tag == ConstantsX.listeningTag) {
    return "listening...";
  }
  else if(tag == ConstantsX.computingTag) {
    return "computing...";
  }
  return "executing...";
}

class App extends StatelessWidget{
  const App({super.key});

  @override
  Widget build(BuildContext context) {
    return ClipRRect(
      borderRadius: BorderRadius.circular(10),
      child: MaterialApp(
        color: ThemeX.backgroundColor,
        debugShowCheckedModeBanner: false,
        home: Scaffold(
          backgroundColor: ThemeX.backgroundColor,
          body: HomeScreen(key: homeScreenKey),
        ),
      ),
    );
  }

}

