import re

def parse_log_line(log_line):
    if 'CHALLENGE_MODE_START' in log_line:
        # zoneName, instanceID, challengeModeID, keystoneLevel, [affixID, ...]
        log_line = log_line.replace('"', '')
        dungeon_details =  log_line.split(',')[1:-3]
        affix_ids_pattern = r'\[([\d,]+)\]'
        match = re.search(affix_ids_pattern, log_line)
        matched_text = match.group(1)
        affix_ids = matched_text = [int(i) for i in matched_text.split(',')]
        return {
            'type': 'CHALLENGE_MODE_START',
            'zone_name': dungeon_details[0],
            'instance_id': int(dungeon_details[1]),
            'affix_ids': affix_ids,
            'key_level': int(dungeon_details[3]),
            'report': True
        }
    if 'CHALLENGE_MODE_END' in log_line:
        # instanceID, success, keystoneLevel, totalTime, keyScore, playerScore
        dungeon_details = log_line.split(',')[1:]
        timer = int(dungeon_details[3])
        if not timer:
            return {
                'type': 'CHALLENGE_MODE_END',
                'report': False
            }

        return {
            'type': 'CHALLENGE_MODE_END',
            'instance_id': int(dungeon_details[0]),
            'success': int(dungeon_details[1]),
            'key_level': int(dungeon_details[2]),
            'timer': timer,
            'key_score': float(dungeon_details[4]),
            'player_score': round(float(dungeon_details[5])),
            'report': True
        }