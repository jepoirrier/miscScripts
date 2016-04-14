/******************************************************************************
 * pixellapse.cpp                                                             *
 *                                                                            *
 * Simple program to capture "pixel-lapse" pictures from a webcam under Linux *
 *                                                                            *
 * (c) Jean-Etienne Poirrier <jepoirrier@gmail.com>, 2008                     *
 * Under GNU General Public License v3.0                                      *
 * More info on http://www.poirrier.be/~jean-etienne/software/pixellapse      *
 *                                                                            *
 * Compile with (2 lines!):                                                   *
 * g++ pixellapse.cpp -o pixellapse                                           *
 * -I /usr/local/include/opencv -L /usr/local/lib -lm -lcv -lhighgui -lcvaux  *
 *                                                                            *
 * History:                                                                   *
 * - 080921: initial version with some hard-coded variables (JEP)             *
 ******************************************************************************/

#include <stdlib.h>
#include <stdio.h>
#include <unistd.h>
#include <math.h>
#include <cv.h>
#include <highgui.h>

using namespace std;

// ********** dotheend() releases the capture and exit program ****************
void dotheend(int errorcode, CvCapture* capture) {

	// release capture
	cvReleaseCapture(&capture);

	// print a more nice end/error message
	printf("End of capture\n");
	switch(errorcode) {
		case 0:
			printf("No error detected :-)\n");
			break;
		case 1:
			printf("Error: wrong usage\nUsage: pixellapse <sleep-time-between-pixel>\n");
			break;
		case 2:
			printf("Error: could not capture an image\n");
			break;
		default:
			printf("Unknown error detected!\n");
	}

	// real exit
	exit(errorcode);
}

// ********** main function ***************************************************
int main(int argc, char *argv[]) {

	// parse command line


	// Definitions & initialisations
	IplImage* img = 0;
	IplImage* imgFinal = 0;
	int frameH, frameW, frameDepth, frameChannels, frameWidthStep, fps, interval; 
	CvCapture* capture = cvCaptureFromCAM(0); // /dev/video0/ YMMV

	frameH = frameW = frameDepth = frameChannels = frameWidthStep = fps = interval = 0;
/*
	if(argc < 2)
		dotheend(1, capture);
	else {
		interval = atoi(argv[1]);
		// TODO better check of argument
	}
*/
	// Get the info for capture
	cvQueryFrame(capture);
	frameH = (int)cvGetCaptureProperty(capture, CV_CAP_PROP_FRAME_HEIGHT);
	frameW = (int)cvGetCaptureProperty(capture, CV_CAP_PROP_FRAME_WIDTH);
	fps  = (int)cvGetCaptureProperty(capture, CV_CAP_PROP_FPS);
	if(fps == -1) {
		fps = 30; // commonly accepted value
		printf("Could not get camera FPS, setting it up to %dfps\n", fps);
	}

	// Set the info for final image by grabbing a sample picture
	if(!cvGrabFrame(capture)) {
		printf("Could not grab sample frame\n");
		dotheend(2, capture);
	}
	img = cvRetrieveFrame(capture);
	frameDepth = img->depth;
	frameChannels = img->nChannels;
	frameWidthStep = img->widthStep;
	printf("Got depth= %d (8 = 8U)\n", frameDepth);
	imgFinal = cvCreateImage(cvSize(frameW, frameH), frameDepth, frameChannels);
	
	// Here we go ...
	printf("Will get %d pixels (for %dx%d picture) every %d seconds\n", frameW*frameH, frameW, frameH, interval);

	//RgbImage imgF(imgFinal);
	// for 1 pixel at a time (time consuming!)
	//for(int i = 0; i < (frameH * frameW); i++) {
	// for 1 line at a time ...
	for(int i = 0; i < frameH; i++) {
		// capture a frame
		img = 0;
		if(!cvGrabFrame(capture)) {
			printf("Could not grab frame %d\n", i);
			dotheend(2, capture);
		}
		img = cvRetrieveFrame(capture);
		//RgbImage imgO(img);
		// take pixel i
		//printf("pixel #%d value: B=%d G=%d R=%d\n", i, img->imageData[(i*3)], img->imageData[(i*3)+1], img->imageData[(i*3)+2]);
		//imgFinal->imageData[(i*3)] = img->imageData[(i*3)];
                //imgFinal->imageData[(i*3)+1] = img->imageData[(i*3)+1];
                //imgFinal->imageData[(i*3)+2] = img->imageData[(i*3)+2];

		// take a row of pixels
		//printf("taking row %d\n", i);
		for(int j = 0; j < frameW; j++) { /*
			imgF[i][j].b = imgO[i][j].b;
			imgF[i][j].g = imgO[i][j].g;
			imgF[i][j].r = imgO[i][j].r; */
			((uchar *)(imgFinal->imageData + i*frameWidthStep))[j*frameChannels + 0] = ((uchar *)(img->imageData + i*frameWidthStep))[j*frameChannels + 0];
			((uchar *)(imgFinal->imageData + i*frameWidthStep))[j*frameChannels + 1] = ((uchar *)(img->imageData + i*frameWidthStep))[j*frameChannels + 1];
			((uchar *)(imgFinal->imageData + i*frameWidthStep))[j*frameChannels + 2] = ((uchar *)(img->imageData + i*frameWidthStep))[j*frameChannels + 2];
		}

		// sleep
		//sleep(interval);
	}

        if(!cvSaveImage("pixellapse.png",imgFinal))
                printf("Could not save: %s\n", "pixellapse.png");

	// Everything has an end
	dotheend(0, capture);
}

