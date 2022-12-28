package com.omegaui.lvc;

import java.io.File;
import java.util.Scanner;

import static com.omegaui.lvc.AppConstants.*;

public class LVCHandler {

    private App app;
    private volatile Process process;

    protected LVCHandler(App app){
        this.app = app;
    }

    protected boolean launch(){
        try {
            process = new ProcessBuilder("linux-voice-control", "--ui=true")
                    .redirectErrorStream(true)
                    .directory(new File(System.getProperty("user.home")))
                    .start();
            buildOutputHandler();
            try{
                Thread.sleep(1000);
                app.setTag(STARTED_TAG);
            }
            catch (Exception e){
                e.printStackTrace();
            }
            return true;
        }
        catch (Exception e){
            e.printStackTrace();
            return false;
        }
    }

    private void buildOutputHandler(){
        new Thread(()->{
            try (Scanner reader = new Scanner(process.getInputStream())) {
                while (process.isAlive()) {
                    while (reader.hasNextLine()) {
                        String line = reader.nextLine();
                        System.out.println(line);
                        if (line.contains("listening")) {
                            app.setStatus("linux-voice-control");
                            app.setTag(LISTENING_TAG);
                        }
                        else if (line.startsWith("saving audio")) {
                            app.setStatus("thinking");
                            app.setTag(COMPUTING_TAG);
                        }
                        else if (line.contains("probability:")) {
                            try{
                                int percentage = Integer.parseInt(line.substring(line.lastIndexOf(',') + 1, line.length() - 1).trim());
                                if(percentage > 60){
                                    app.setTag(EXECUTING_TAG);
                                    app.setStatus("found a perfect match");
                                }
                                else{
                                    app.setStatus("no match found");
                                }
                            }
                            catch (Exception e){
                                //do nothing
                            }
                        }
                        else if (line.equals("no voice")) {
                            app.setStatus("empty clip");
                        }
                        else if (line.equals("no speech in clip")) {
                            app.setStatus("no voice in clip");
                        }
                    }
                }
            }
            catch (Exception ex){
                ex.printStackTrace();
            }
            System.exit(0);
        }, "app-output-handler").start();
    }

}
