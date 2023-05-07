Folder "testcase_source" inludes:
	+ sample_image
	+ sample_text_ground_truth: lines of text in some format



Folder "result" includes:
	+ test_image : what i have detected, it includes:
		- red_boxes: i draw based on 'sample_text_ground_truth'
		- blue_boxes: i draw based on what i detected	

	+ iou_image: illustrate the accuracy of what i predicted and ground_truth	

	+ test_text: predicted lines of text in format

	***NOTE: only boxes with "IOU > 0.4" are drawn

	

Folder "log" includes: 
	+ log_text: information of each line includes :
		- IOU (from 0 to 1) ,   matching text percentage (from 0 to 100)
		- grounth_truth_text
		- test_text
		
		- !-ERROR ... : flag indicate that line cannot predicted
		
		- summerization: at the end, summerize Average IOU, Text Matching of WHOLE receipt/bill


	***NOTE: i only check 'matching text %' only if that line can be detected.
		Otherwise,  'matching text %' is not calculated and added to summerization
