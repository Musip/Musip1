//
//  SecondViewController.h
//  Musip_Recorder
//
//  Created by 哲鑫 韩 on 11/21/16.
//  Copyright © 2016 Haoming Liu. All rights reserved.
//

#ifndef SecondViewController_h
#define SecondViewController_h


#import <UIKit/UIKit.h>

//
// First import the EZAudio header
//
#include "EZAudio/EZAudio.h"

//
// Here's the default audio file included with the example
//
#define kAudioFileDefault [[NSBundle mainBundle] pathForResource:@"Joy_Mismatch3" ofType:@"m4a"]

//------------------------------------------------------------------------------
#pragma mark - SecondViewController
//------------------------------------------------------------------------------

@interface SecondViewController : UIViewController <EZAudioPlayerDelegate>

//------------------------------------------------------------------------------
#pragma mark - Properties
//------------------------------------------------------------------------------

//
// An EZAudioFile that will be used to load the audio file at the file path specified
//
@property (nonatomic, strong) EZAudioFile *audioFile;

//------------------------------------------------------------------------------

//
// An EZAudioPlayer that will be used for playback
//
@property (nonatomic, strong) EZAudioPlayer *player;

//------------------------------------------------------------------------------

//
// The CoreGraphics based audio plot
//
@property (nonatomic, weak) IBOutlet EZAudioPlotGL *audioPlot;

//------------------------------------------------------------------------------

//
// A label to display the current file path with the waveform shown
//
@property (nonatomic, weak) IBOutlet UILabel *filePathLabel;

//------------------------------------------------------------------------------

//
// A slider to indicate the current frame position in the audio file
//
@property (nonatomic, weak) IBOutlet UISlider *positionSlider;

//------------------------------------------------------------------------------

//
// A slider to indicate the rolling history length of the audio plot.
//
@property (nonatomic, weak) IBOutlet UISlider *rollingHistorySlider;

//------------------------------------------------------------------------------

//
// A slider to indicate the volume on the audio player
//
@property (nonatomic, weak) IBOutlet UISlider *volumeSlider;

//
// Match is an array passed from main view controller
//
@property (nonatomic) NSArray *match;

//
// The audio file name to be played
//
@property (nonatomic) NSURL *url;

//
//
//
@property (nonatomic) int length;

//------------------------------------------------------------------------------
#pragma mark - Actions
//------------------------------------------------------------------------------

//
// Switches the plot drawing type between a buffer plot (visualizes the current
// stream of audio data from the update function) or a rolling plot (visualizes
// the audio data over time, this is the classic waveform look)
//
- (IBAction)changePlotType:(id)sender;

//------------------------------------------------------------------------------

//
// Changes the length of the rolling history of the audio plot.
//
- (IBAction)changeRollingHistoryLength:(id)sender;

//------------------------------------------------------------------------------

//
// Changes the volume of the audio player.
//
- (IBAction)changeVolume:(id)sender;

//------------------------------------------------------------------------------

//
// Begins playback if a file is loaded. Pauses if the file is already playing.
//
- (IBAction)play:(id)sender;

//------------------------------------------------------------------------------

//
// Seeks to a specific frame in the audio file.
//
- (IBAction)seekToFrame:(id)sender;

@end

#endif /* SecondViewController_h */
