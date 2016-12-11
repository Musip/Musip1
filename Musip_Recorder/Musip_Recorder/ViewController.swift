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

class ViewController: UIViewController, AVAudioPlayerDelegate, AVAudioRecorderDelegate, UIPickerViewDelegate, UIPickerViewDataSource {
    
    @IBOutlet var RecordButton: UIButton!
    @IBOutlet var PlayButton: UIButton!
    @IBOutlet weak var UploadButton: UIButton!
    @IBOutlet weak var PauseButton: UIButton!
    @IBOutlet weak var ScoreLabel: UILabel!
    @IBOutlet weak var ActivityIndicator: UIActivityIndicatorView!
    
    @IBOutlet weak var ShowButton: UIButton!
    
    @IBOutlet weak var ReferencePicker: UIPickerView!
    var reference = ["Ode to Joy"]
    var selectedReference : String = ""
    
    private var blocker = UIView()
    var recorder : AVAudioRecorder!
    var player : AVAudioPlayer!
    var fileName = "audioFile.m4a"
    var osi = AKOscillator()
    var matchResult : [Int]!
    var scores : Double!
    
    override func viewDidLoad() {
        super.viewDidLoad()
        // Do any additional setup after loading the view, typically from a nib.
        setUpRecoeder()
        
        self.ActivityIndicator.hidesWhenStopped = true
        
        self.view.backgroundColor = UIColor(patternImage: UIImage(named: "background.jpg")!)
        
        if self.scores != nil {
            self.ScoreLabel.text = String(format:"%.2f", self.scores)
        } else {
            self.ScoreLabel.text = "0.0"
        }
        
        self.ReferencePicker.delegate = self
        self.ReferencePicker.dataSource = self
    }
    
    func numberOfComponents(in pickerView: UIPickerView) -> Int {
        return 1
    }
    
    func pickerView(_ pickerView: UIPickerView, numberOfRowsInComponent component: Int) -> Int {
        return self.reference.count
    }
    
    func pickerView(_ pickerView: UIPickerView, titleForRow row: Int, forComponent component: Int) -> String? {
        return self.reference[row]
    }
    
    func pickerView(_ pickerView: UIPickerView, didSelectRow row: Int, inComponent component: Int) {
        self.selectedReference = self.reference[row]
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
            "userId"    : "0",
            "reference" : self.selectedReference
        ]
        
        let boundary = generateBoundaryString()
        
        request.setValue("multipart/form-data; boundary=\(boundary)", forHTTPHeaderField: "Content-Type")
        
        
        let audioData = NSData(contentsOf : getFileUrl())
        
        if(audioData == nil) {
            return;
        }
        
        request.httpBody = createBodyWithParameters(parameters: param, filePathKey: "file", audioDataKey: audioData!, boundary: boundary) as Data
        
        ActivityIndicator.startAnimating()
        self.disableAllButtons()
        
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
                
                self.scores = json?["scores"] as! Double
                self.ScoreLabel.text = String(format:"%.2f", self.scores)
                
                self.ActivityIndicator.stopAnimating()
                self.enableAllButtons()
                
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
    
    func disableAllButtons() {
        self.RecordButton.isEnabled = false
        self.PlayButton.isEnabled = false
        self.UploadButton.isEnabled = false
        self.PauseButton.isEnabled = false
        self.ShowButton.isEnabled = false
    }
    
    func enableAllButtons() {
        self.RecordButton.isEnabled = true
        self.PlayButton.isEnabled = true
        self.UploadButton.isEnabled = true
        self.PauseButton.isEnabled = true
        self.ShowButton.isEnabled = true
    }
}

extension NSMutableData {
    
    func appendString(string: String) {
        let data = string.data(using: String.Encoding.utf8, allowLossyConversion: true)
        append(data!)
    }
}


