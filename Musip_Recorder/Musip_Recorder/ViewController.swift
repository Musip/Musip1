//
//  ViewController.swift
//  Musip_Recorder
//
//  Created by Haoming Liu on 11/4/16.
//  Copyright © 2016 Haoming Liu. All rights reserved.
//

import UIKit
import AVFoundation

class ViewController: UIViewController, AVAudioPlayerDelegate, AVAudioRecorderDelegate {
    
    @IBOutlet var RecordButton: UIButton!
    @IBOutlet var PlayButton: UIButton!
    
    var recorder : AVAudioRecorder!
    var player : AVAudioPlayer!
    var fileName = "audioFile.m4a"
    
    override func viewDidLoad() {
        super.viewDidLoad()
        // Do any additional setup after loading the view, typically from a nib.
        setUpRecoeder()
    }
    
    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
        // Dispose of any resources that can be recreated.
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
    
    func audioPlayerDidFinishPlaying(_ player: AVAudioPlayer, successfully flag: Bool) {
        PlayButton.setTitle("Play", for: .normal)
        RecordButton.isEnabled = true
    }
}


