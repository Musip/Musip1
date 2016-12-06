//
//  ViewController.swift
//  Musip_Recorder
//
//  Created by Haoming Liu on 11/4/16.
//  Copyright © 2016 Haoming Liu. All rights reserved.
//

import UIKit
import AVFoundation
import AudioKit

class ViewController: UIViewController, AVAudioPlayerDelegate, AVAudioRecorderDelegate {
    
    @IBOutlet var RecordButton: UIButton!
    @IBOutlet var PlayButton: UIButton!
    @IBOutlet weak var UploadButton: UIButton!
    @IBOutlet weak var PauseButton: UIButton!
    @IBOutlet weak var ScoreLabel: UILabel!
    
    var recorder : AVAudioRecorder!
    var player : AVAudioPlayer!
    var fileName = "audioFile.m4a"
    var osi = AKOscillator()
    var matchResult : [Int]!
    
    override func viewDidLoad() {
        super.viewDidLoad()
        // Do any additional setup after loading the view, typically from a nib.
        setUpRecoeder()
    }
    
    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
        // Dispose of any resources that can be recreated.
    }
    
    override func prepare(for segue: UIStoryboardSegue, sender: Any?) {
        if (segue.identifier == "segueToDisplayer") {
            let second:SecondViewController = segue.destination as! SecondViewController
            second.match = matchResult
            second.url = getFileUrl()
            second.length = Int32(matchResult.count)
        }
    }
    
    func setUpRecoeder() {
        let recordSettings = [AVFormatIDKey : kAudioFormatAppleLossless,
                              AVEncoderAudioQualityKey: AVAudioQuality.max.rawValue,
                              AVEncoderBitRateKey : 320000,
                              AVNumberOfChannelsKey : 2,
                              AVSampleRateKey : 44100.0 ] as [String : Any]
        
        do {
            recorder = try AVAudioRecorder(url : getFileUrl(), settings : recordSettings)
            
            recorder.delegate = self
            recorder.prepareToRecord()
        } catch {
            print(error)
        }
    }
    
    func getCacheDirectory() -> URL {
        let paths = FileManager.default.urls(for: .documentDirectory, in: .userDomainMask)
        let documentsDirectory = paths[0]
        return documentsDirectory
    }
    
    func getFileUrl() -> URL {
        let path = getCacheDirectory().appendingPathComponent(fileName)
        return path
    }
    
    func preparePlayer() {
        do {
            player = try AVAudioPlayer(contentsOf : getFileUrl())
            
            player.delegate = self
            player.prepareToPlay()
            player.volume = 1.0
        } catch {
            print(error)
        }
    }
    
    @IBAction func Play(_ sender: UIButton) {
        if sender.titleLabel?.text == "Play" {
            preparePlayer()
            player.play()
            sender.setTitle("Stop", for: .normal)
            RecordButton.isEnabled = false
        } else {
            player.stop()
            player.currentTime = 0
            sender.setTitle("Play", for: .normal)
            RecordButton.isEnabled = true
        }
    }
    
    @IBAction func Record(_ sender: UIButton) {
        if sender.titleLabel?.text == "Record" {
            recorder.record()
            sender.setTitle("Stop", for: .normal)
            PlayButton.isEnabled = false
        } else {
            recorder.stop()
            sender.setTitle("Record", for: .normal)
            PlayButton.isEnabled = true
        }
    }
    
    @IBAction func Pause(_ sender: UIButton) {
        if player.isPlaying == true {
            player.stop()
            sender.setTitle("Resume", for: .normal)
        } else {
            player.play()
            sender.setTitle("Pause", for: .normal)
        }
    }
    
    func audioPlayerDidFinishPlaying(_ player: AVAudioPlayer, successfully flag: Bool) {
        PlayButton.setTitle("Play", for: .normal)
        RecordButton.isEnabled = true
    }
    
    @IBAction func uploadAudio(_ sender: UIButton) {
        let destURL = NSURL(string: "http://localhost:8000/cgi-bin/audio_receiver.py"); // change later
        // let filePathURL = NSURL(fileURLWithPath: fileName)
        
        let request = NSMutableURLRequest(url:destURL! as URL);
        request.httpMethod = "POST";
        
        let param = [
            "firstName"  : "Haoming",
            "lastName"    : "Liu",
            "userId"    : "0"
        ]
        
        let boundary = generateBoundaryString()
        
        request.setValue("multipart/form-data; boundary=\(boundary)", forHTTPHeaderField: "Content-Type")
        
        
        let audioData = NSData(contentsOf : getFileUrl())
        
        if(audioData == nil) {
            return;
        }
        
        request.httpBody = createBodyWithParameters(parameters: param, filePathKey: "file", audioDataKey: audioData!, boundary: boundary) as Data
        
        let task = URLSession.shared.dataTask(with: request as URLRequest) {
            data, response, error in
            
            if error != nil {
                print("error=\(error)")
                return
            }
            
            // Print out response object
            print("******* response = \(response)")
            
            // Print out reponse body
            let responseString = NSString(data: data!, encoding: String.Encoding.utf8.rawValue)
            print("****** response data = \(responseString!)")
            
            do {
                // use the data later
                let json = try JSONSerialization.jsonObject(with: data!, options: []) as? NSDictionary
                self.matchResult = json?["matches"] as! [Int]
                var total = 0.0
                var wrong = 0.0
                for result in self.matchResult {
                    if result != 0 {
                        wrong = wrong + 1
                    }
                    total = total + 1
                }
                self.ScoreLabel.text = String(format:"%.2f", (total - wrong) / total * 100)
            } catch {
                print(error)
            }
        }
        
        task.resume()
    }
    
    func generateBoundaryString() -> String {
        return "Boundary-\(NSUUID().uuidString)"
    }
    
    func createBodyWithParameters(parameters: [String: String]?, filePathKey: String?, audioDataKey: NSData, boundary: String) -> NSData {
        let body = NSMutableData();
        
        if parameters != nil {
            for (key, value) in parameters! {
                body.appendString(string: "--\(boundary)\r\n")
                body.appendString(string: "Content-Disposition: form-data; name=\"\(key)\"\r\n\r\n")
                body.appendString(string: "\(value)\r\n")
            }
        }
        
        let filename = fileName
        let mimetype = "audio/mpeg"
        
        body.appendString(string: "--\(boundary)\r\n")
        body.appendString(string: "Content-Disposition: form-data; name=\"\(filePathKey!)\"; filename=\"\(filename)\"\r\n")
        body.appendString(string: "Content-Type: \(mimetype)\r\n\r\n")
        body.append(audioDataKey as Data)
        body.appendString(string: "\r\n")
        
        
        
        body.appendString(string: "--\(boundary)--\r\n")
        
        return body
    }
}

extension NSMutableData {
    
    func appendString(string: String) {
        let data = string.data(using: String.Encoding.utf8, allowLossyConversion: true)
        append(data!)
    }
}


