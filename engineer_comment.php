<?php
/*
 *  Programmer	: Fariz Dwi Pratama
 *  Email		: fariz_d_pratama@telkomsel.co.id
 *  Telegram	: @frzdp
 *  ____________________________________________________________
 *
 *  File		: auto_ec.php
 *  Purpose		: auto create engineer comment Monita Area 1
 *  ____________________________________________________________
 *
 *  Updated		: August 18, 2018
 *	Version		: 1.0.5
 *  ____________________________________________________________
 *
 *	Log			:
 *				- July 13-14, 2018	: 1.0.0 Release
 *				- July 15, 2018		: 1.0.1 Add cURL
 *				- July 16, 2018		: 1.0.2 Add scheduling
 *				- July 19, 2018		: 1.0.3 Optimize, add report to BOT Telegram
 *				- July 20, 2018		: 1.0.4 Fixed bug
 *				- August 18, 2018	: 1.0.5 + Optimize
 *											+ Delete report to BOT Telegram
 *											+ Add scheduling every 15 minutes
 *											+ Change free text from ! with full stop (.)
 *											+ Change time limit command power off from 240 to 120 minutes
 *											+ Change from RTPO to Department
 *											+ Change command site with genset direct to transmission
 *											+ Change pic to each wali site
*/

#insialiasi
$regional = 'Sumbagteng';
$nsa = 'Padang';
$batas = 120;
$remark = '.';

#Monita
$web = '***Link***?action=All-All-All-All&filter[0][field]=regional_name&filter[0][data][type]=string&filter[0][data][value]='.$regional.'&filter[1][field]=departement_name&filter[1][data][type]=string&filter[1][data][value]='.$nsa;

#--alarm Full, Genset
$monita[0] = $web.'&filter[2][field]=status_alarm&filter[2][data][type]=string&filter[2][data][value]=Full&filter[3][field]=jenis_catuan&filter[3][data][type]=string&filter[3][data][value]=Genset&filter[4][field]=freetext_full&filter[4][data][type]=string&filter[4][data][value]=Oss Alarm&page=1&start=0&limit=20';
#--alarm Partial
$monita[1] = $web.'&filter[2][field]=status_alarm&filter[2][data][type]=string&filter[2][data][value]=Partial&filter[3][field]=freetext_full&filter[3][data][type]=string&filter[3][data][value]=Oss Alarm&page=1&start=0&limit=20';
$monita[2] = $web.'&filter[2][field]=status_alarm&filter[2][data][type]=string&filter[2][data][value]=Partial&filter[3][field]=freetext_full&filter[3][data][type]=string&filter[3][data][value]=POWER OFF&page=1&start=0&limit=20';
#--alarm Full, Power OFF
$monita[3] = $web.'&filter[2][field]=status_alarm&filter[2][data][type]=string&filter[2][data][value]=Full&filter[3][field]=freetext_full&filter[3][data][type]=string&filter[3][data][value]=POWER OFF&page=1&start=0&limit=20';
#--alarm Full, Non Genset
$monita[4] = $web.'&filter[2][field]=status_alarm&filter[2][data][type]=string&filter[2][data][value]=Full&filter[3][field]=freetext_full&filter[3][data][type]=string&filter[3][data][value]=Oss Alarm&page=1&start=0&limit=20';

#function
function datajson($web) {
	$web = str_replace(' ', '%20', $web);
	$output = file_get_contents($web);
	$replace = array(
		'success:' => '"success":',
		'jml:' => '"jml":',
		'data:' => '"data":'
	);
	$data = strtr($output, $replace);
	$data_json = json_decode($data);
	return $data_json;
}

function walisite($pic) {
	switch ($pic) {
		case 'Fariz Dwi Pratama':
			$wali = 'farizpra';
			break;
		
		case 'Ihsan':
			$wali = 'ihsannug';
			break;

		case 'Fauzan Akbar':
			$wali = 'fauzanakb';
			break;

		case 'Arianto Sirandan':
			$wali = 'ariantosir';
			break;

		case 'I Gaap Kusuma':
			$wali = 'IKuu';
			break;

		case 'Guntur Eko Putro':
			$wali = 'gunturput';
			break;

		case 'Rafelly Jhon':
			$wali = 'rafellyj';
			break;

		case 'Ahmad Fuad':
			$wali = 'gunturput';
			break;

		default:
			$wali = 'r10_omc_1';
			break;
	}
	return $wali;
}

function comment($ticket, $kode, $pic, $btsid, $tglalarm, $status, $remark) {
  $web = '***Link Backend***?id_ticket='.$ticket.'&id_pc='.$kode.'&alias='.$pic.'&freetext='.$remark.'&input_from=Web Monita&status_kirim_email=NO&flag=&bts_id='.$btsid.'&tgl_alarm='.$tglalarm.'&status_alarm='.$status;
  $web = str_replace(' ', '%20', $web);
  $ch = curl_init();
  curl_setopt($ch, CURLOPT_RETURNTRANSFER, TRUE);
  curl_setopt($ch, CURLOPT_USERAGENT, "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.1a2pre) Gecko/2008073000 Shredder/3.0a2pre ThunderBrowse/3.2.1.8");
  curl_setopt($ch, CURLOPT_TIMEOUT, 90);
  curl_setopt($ch, CURLOPT_URL, $web);
	curl_setopt($ch, CURLOPT_POST, TRUE);
  ob_start();
  curl_exec($ch);
  ob_end_clean();
  curl_close($ch);
}

function myloop($web, $batas, $remark) {
  // Alarm Full Down & Genset
  $data_1 = datajson($web[0]);
	if (isset($data_1->data)) {
		for ($i = 0; $i < $data_1->jml; $i++) {
			$pic = walisite($data_1->data[$i]->wali_name);
			comment($data_1->data[$i]->id_ticket, '25', $pic, $data_1->data[$i]->bts_id, $data_1->data[$i]->tgl_alarm, $data_1->data[$i]->status_alarm, $remark);
		}
	}
	
	// Alarm Partial
	$data_2 = datajson($web[1]);
	if (isset($data_2->data)) {
		for ($i = 0; $i < $data_2->jml; $i++) {
			$pic = walisite($data_2->data[$i]->wali_name);
			comment($data_2->data[$i]->id_ticket, '58', $pic, $data_2->data[$i]->bts_id, $data_2->data[$i]->tgl_alarm, $data_2->data[$i]->status_alarm, $remark);
		}
	}
	$data_3 = datajson($web[2]);
	if (isset($data_3->data)) {
		for ($i = 0; $i < $data_3->jml; $i++) {
			$pic = walisite($data_3->data[$i]->wali_name);
			comment($data_3->data[$i]->id_ticket, '58', $pic, $data_3->data[$i]->bts_id, $data_3->data[$i]->tgl_alarm, $data_3->data[$i]->status_alarm, $remark);
		}
	}

	// Alarm Full Down & Power Off
	$data_4 = datajson($web[3]);
	if (isset($data_4->data)) {
		for ($i = 0; $i < $data_4->jml; $i++) {
			$menit = ((int)substr($data_4->data[$i]->aging, 0, 2) * 60) + (int)substr($data_4->data[$i]->aging, -5, -3);
			if ($menit > $batas) {
				$pic = walisite($data_4->data[$i]->wali_name);
				comment($data_4->data[$i]->id_ticket, '25', $pic, $data_4->data[$i]->bts_id, $data_4->data[$i]->tgl_alarm, $data_4->data[$i]->status_alarm, $remark);
			}
		}
	}

	// Alarm Full Down & Non Genset
	$data_5 = datajson($web[4]);
	if (isset($data_5->data)) {
		for ($i = 0; $i < $data_5->jml; $i++) {
			$menit = ((int)substr($data_5->data[$i]->aging, 0, 2) * 60) + (int)substr($data_5->data[$i]->aging, -5, -3);
			if ($menit < $batas) {
				$k = '7';
			} else {
				$k = '25';
			}
			$pic = walisite($data_5->data[$i]->wali_name);
			comment($data_5->data[$i]->id_ticket, $k, $pic, $data_5->data[$i]->bts_id, $data_5->data[$i]->tgl_alarm, $data_5->data[$i]->status_alarm, $remark);
		}
	}
}

#looping process
while (true) {
	$menit = date('i');
	if ($menit == '00' or $menit == '15' or $menit == '30' or $menit == '45') {
		myloop($monita, $batas, $remark);
	}
	sleep(60);
}
