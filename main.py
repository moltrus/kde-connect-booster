import kde_c_features as kde_c_f
import argparse as ap
import json
import os

currect_dir = os.path.dirname(os.path.realpath(__file__))
CONFIG_PATH = os.path.join(currect_dir, 'config.json')

config_file = open(CONFIG_PATH,'r')
configation = json.load(config_file)
config_file.close()

parser = ap.ArgumentParser()

parser.add_argument("--ring_pc",action='store_true')
parser.add_argument("--stop_ring",action='store_true')
parser.add_argument("--shutdown",action='store_true')
parser.add_argument("--restart",action='store_true')
parser.add_argument("--hibernate",action='store_true')
parser.add_argument("--lock",action='store_true')
parser.add_argument("--grab_picture",action='store_true')
parser.add_argument("--screenshot",action='store_true')
parser.add_argument("--grab_video",action='store_true')
parser.add_argument("--record_audio",action='store_true')

args = parser.parse_args()

if args.ring_pc:
	duration = configation['ring_duration']
	kde_c_f.ring_pc(duration=duration)

if args.stop_ring:
	kde_c_f.stop_ringing_pc()

if args.shutdown:
	delay = configation['shutdown_delay']
	kde_c_f.shutdown_pc(delay=delay)

if args.restart:
	kde_c_f.restart_pc()

if args.hibernate:
	kde_c_f.hibernate_pc()

if args.lock:
	kde_c_f.lock_pc()

if args.grab_picture:
	save_dir = eval(configation['save_dir'])
	is_high_res = configation['high_resolution']
	kde_c_f.grab_picture(save_dir=save_dir,is_high_res=is_high_res)

if args.screenshot:
	save_dir = eval(configation['save_dir'])
	kde_c_f.grab_screen(save_dir=save_dir)

if args.grab_video:
	save_dir = eval(configation['save_dir'])
	duration = configation['video_duration']
	kde_c_f.grab_video(save_dir=save_dir,duration=duration)

if args.record_audio:
	save_dir = eval(configation['save_dir'])
	duration = configation['audio_duration']
	kde_c_f.record_audio(save_dir=save_dir,duration=duration)
