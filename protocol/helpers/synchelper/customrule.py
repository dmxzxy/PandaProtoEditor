#!/usr/bin/env python
# -*- encoding:utf8 -*-

# 这个文件是根据项目来更改的文件 

import sys
import re
import loghelper.logger as logger
from string import strip

from protocol.helpers.panpbtool.conf import protolabel
from protocol.helpers.panpbtool.data.baserule import baserule

MissingProtoList = {}
MissingProtoList["C2SUserQueryDelivableOrderProto"] = 1074
MissingProtoList["S2CUserQueryDelivableOrderRetProto"] = 1074
MissingProtoList["C2SUserRankArenaV2ListProto"] = 1931
MissingProtoList["S2CUserRankArenaV2ListRetProto"] = 1931
MissingProtoList["C2SUserActivityTaskDailyRewardObtainProto"] = 2046
MissingProtoList["S2CUserActivityTaskDailyRewardRetProto"] = 2046
MissingProtoList["S2CUserTapeMsgGetRecvTapesRetProto"] = 2480
MissingProtoList["S2CUserTapeMsgListenTapeRetProto"] = 2481
MissingProtoList["S2CUserSubscriptExpireChangeProto"] = 5213
MissingProtoList["C2SUserActivityDefendTaskRewardProto"] = 4006
MissingProtoList["S2CUserActivityDefendTaskRewardRetProto"] = 4006
MissingProtoList["S2CUserResDungeonUpdateDefenceRetProto"] = 2814
MissingProtoList["S2CUserResDungeonThemeBattleGobackRetProto"] = 2815
MissingProtoList["C2SUserActivityAnswerExamProto"] = 4007
MissingProtoList["S2CUserActivityAnswerExamRetProto"] = 4007
MissingProtoList["C2SUserActivityReviewExamProto"] = 4008
MissingProtoList["S2CUserActivityReviewExamRetProto"] = 4008
MissingProtoList["C2SUserEventStorySubmitProto"] = 4009
MissingProtoList["S2CUserEventStorySubmitRetProto"] = 4009
MissingProtoList["C2SUserTuJianSubmitProto"] = 4010
MissingProtoList["S2CUserTuJianSubmitRetProto"] = 4010
MissingProtoList["C2SUserObtainBuffRewardProto"] = 4012
MissingProtoList["S2CUserObtainBuffRewardRetProto"] = 4012
MissingProtoList["C2SUserSingleCardGoodsBuyProto"] = 4013
MissingProtoList["S2CUserSingleCardGoodsBuyRetProto"] = 4013
MissingProtoList["C2SUserObtainTuJianRewardProto"] = 4011
MissingProtoList["S2CUserObtainTuJianRewardRetProto"] = 4011
MissingProtoList["C2SUserActivityAnswerExam3Proto"] = 4025
MissingProtoList["S2CUserActivityAnswerExam3RetProto"] = 4025
MissingProtoList["C2SUserActivityReviewExam3Proto"] = 4026
MissingProtoList["S2CUserActivityReviewExam3RetProto"] = 4026
MissingProtoList["C2SUserHomeStartDispatchReqProto"] = 2871
MissingProtoList["S2CUserHomeStartDispatchReqRetProto"] = 2871
MissingProtoList["C2SUserHomeSpeedUpDispatchMissionReqProto"] = 2872
MissingProtoList["S2CUserHomeSpeedUpDispatchMissionReqRetProto"] = 2872
MissingProtoList["C2SUserHomeObtainDispatchRewardReqProto"] = 2873
MissingProtoList["S2CUserHomeObtainDispatchRewardReqRetProto"] = 2873
MissingProtoList["C2SUserHomeCancelDispatchMissionReqProto"] = 2874
MissingProtoList["S2CUserHomeCancelDispatchMissionReqRetProto"] = 2874
MissingProtoList["C2SUserHomeRefreshDispatchMissionReqProto"] = 2875
MissingProtoList["S2CUserHomeRefreshDispatchMissionReqRetProto"] = 2875
MissingProtoList["C2SUserH5WebviewRequestProto"] = 6001
MissingProtoList["S2CUserH5WebviewRequestProto"] = 6001
MissingProtoList["C2SUserChapterBoxFinishProto"] = 1141
MissingProtoList["S2CUserChapterBoxFinishRetProto"] = 1141
MissingProtoList["S2CUserPushPackActivitiesInfoNotify"] = 5262
MissingProtoList["S2CUserHomeRandRewardUnitsNotify"] = 5263
MissingProtoList["S2CUserActivityLivenessAddupSubmittRetProto"] = 4032
MissingProtoList["C2SUserBillboardMaleStateProto"] = 2902
MissingProtoList["S2CUserBillboardMaleStateRetProto"] = 2902
MissingProtoList["C2SUserExchangeGoodsProto"] = 4051
MissingProtoList["S2CUserExchangeGoodsRetProto"] = 4051
MissingProtoList["C2SUserExchangeStoreRefreshProto"] = 4052
MissingProtoList["S2CUserExchangeStoreRefreshRetProto"] = 4052
MissingProtoList["C2SUserActivityMayDayVoteSubmitProto"] = 4200
MissingProtoList["C2SUserActivityMayDayRewardTitleSubmitProto"] = 4201
MissingProtoList["C2SUserActivityNewBirthDayReadStoryProto"] = 4045
MissingProtoList["S2CUserActivityNewBirthDayReadStoryRetProto"] = 4045
MissingProtoList["S2CUserPublishMsgNtfProto"] = 5269
MissingProtoList["C2SUserActivitySpringFestivalPieceGainProto"] = 4061
MissingProtoList["S2CUserActivitySpringFestivalPieceGainRetProto"] = 4061
MissingProtoList["C2SUserActivitySpringFestivalPieceShareProto"] = 4062
MissingProtoList["S2CUserActivitySpringFestivalPieceShareRetProto"] = 4062
MissingProtoList["C2SUserActivitySpringFestivalPieceShareRewardProto"] = 4063
MissingProtoList["S2CUserActivitySpringFestivalPieceShareRewardRetProto"] = 4063
MissingProtoList["C2SUserActivitySpringFestivalPieceOpenRewardProto"] = 4064
MissingProtoList["S2CUserActivitySpringFestivalPieceOpenRewardProto"] = 4064
MissingProtoList["C2SUserActivityDragonBoatPieceGainProto"] = 4301
MissingProtoList["S2CUserActivityDragonBoatPieceGainRetProto"] = 4301
MissingProtoList["C2SUserActivityDragonBoatPieceRewardProto"] = 4302
MissingProtoList["S2CUserActivityDragonBoatPieceRewardRetProto"] = 4302
MissingProtoList["C2SUserActivityDragonBoatPieceOpenRewardProto"] = 4303
MissingProtoList["S2CUserActivityDragonBoatPieceOpenRewardProto"] = 4303
MissingProtoList["C2SUserActivityDoubleActivityRewardProto"] = 4071
MissingProtoList["S2CUserActivityDoubleActivityRewardRetProto"] = 4071
MissingProtoList["S2CUserActivityDoubleActivityRefreshNotify"] = 5270
MissingProtoList["C2SUserActivityDoubleActivityCumulationRewardProto"] = 4072
MissingProtoList["S2CUserActivityDoubleActivityCumulationRewardRetProto"] = 4072
MissingProtoList["S2CUserActivityDoubleActivityReturnPresentNotify"] = 5271
MissingProtoList["C2SUserYsdkGetBalanceProto"] = 4090
MissingProtoList["S2CUserYsdkGetBalanceRetProto"] = 4090
MissingProtoList["S2CUserClientHotfixNotify"] = 5272
MissingProtoList["C2SUserActivitySnowTaskMergeProto"] = 4100
MissingProtoList["S2CUserActivitySnowTaskMergeRetProto"] = 4100
MissingProtoList["C2SUserActivitySnowTaskShareProto"] = 4101
MissingProtoList["S2CUserActivitySnowTaskShareRetProto"] = 4101
MissingProtoList["C2SUserActivitySnowTaskWatchPVProto"] = 4102
MissingProtoList["S2CUserActivitySnowTaskWatchPVRetProto"] = 4102
MissingProtoList["C2SUserActivitySnowTaskShareRewardProto"] = 4103
MissingProtoList["S2CUserActivitySnowTaskShareRewardRetProto"] = 4103
MissingProtoList["S2CUserResourceSecretKeyNotify"] = 5273
MissingProtoList["C2SUserChapterChangeRuleProto"] = 4111
MissingProtoList["S2CUserChapterChangeRuleRetProto"] = 4111
MissingProtoList["C2SUserChapterRewardProto"] = 4110
MissingProtoList["S2CUserChapterRewardRetProto"] = 4110
MissingProtoList["C2SUserActivityExtraPiecesShareProto"] = 4141
MissingProtoList["C2SUserActivityExtraPiecesShareRewardProto"] = 4141
MissingProtoList["C2SUserFriendsItemWishPublishProto"] = 4120
MissingProtoList["S2CUserFriendsItemWishPublishRetProto"] = 4120
MissingProtoList["C2SUserFriendsItemWishSendProto"] = 4121
MissingProtoList["S2CUserFriendsItemWishSendRetProto"] = 4121
MissingProtoList["S2CUserFriendsItemWishReceiveNotify"] = 5275
MissingProtoList["C2SUserFriendsItemWishDifferentFriendsRewardProto"] = 4122
# MissingProtoList["C2SUserActivityBattlepassRewardSubmitProto"] = -1
# MissingProtoList["S2CUserActivityBattlepassRewardSubmitRetProto"] = -1
MissingProtoList["C2SUserSpecialStoryGetRecvStoriesProto"] = 4055
MissingProtoList["S2CUserSpecialStoryGetRecvStoriesRetProto"] = 4055
MissingProtoList["C2SUserSpecialStoryReadProto"] = 1081
MissingProtoList["S2CUserSpecialStoryReadRetProto"] = 1081
MissingProtoList["C2SUserChangeTitleProto"] = 1081
MissingProtoList["S2CUserChangeTitleRetProto"] = 1081
MissingProtoList["S2CMaydayCrossDayNotify"] = 5276
MissingProtoList["C2SMaydayTravelProto"] = 4150
MissingProtoList["S2CMaydayTravelRetProto"] = 4150
MissingProtoList["C2SMaydayTravelFinishProto"] = 4151
MissingProtoList["S2CMaydayTravelFinishRetProto"] = 4151
MissingProtoList["S2CUserExtraStageLineInfoNtf"] = 5278


class customrule(baserule):
    context = None
    def __init__(self, context):
        self.context = context
        fp = open(context.write_path + "/protomsg.go", "r")
        id_descript_data = fp.read()
        fp.close()
        context.id_descript_data = id_descript_data

    def get_namespace(self):
        context = self.context
        raw_data = context.raw_data
        if not hasattr(context, "namespace"):
            project_namespace = ""
            for proto_file in raw_data.proto_file:
                project_namespace = proto_file.package
                index = project_namespace.rfind('.')
                if index != -1:
                    project_namespace = project_namespace[0:index]
                break
            context.namespace = project_namespace
        return context.namespace

    def get_module_name(self, module_desc):
        namespace = self.get_namespace()
        name = module_desc.package[(len(namespace)+1):]
        if len(name) == 0:
            return "global"
        return name

    def is_protocol(self, message_desc):
        message_name = message_desc.name

        if message_name.startswith('C2S'):
            return True
            
        if message_name.startswith('S2C'):
            return True

        return False

    def get_protocol_id(self, message_desc):
        context = self.context
        if not hasattr(context, "proto_ids"):
            id_descript_data = context.id_descript_data
            digi_str = re.findall(r'.*=.*', id_descript_data, re.MULTILINE)
            proto_ids = {}
            for _str in digi_str:
                _comment = ''
                _ret = re.findall(r'\/\/[^\n]*', _str, re.MULTILINE)
                if len(_ret) > 0:
                    _str = _str.replace(_ret[0], '')
                    _comment = _ret[0]
                _ret = re.findall(r'(.*)=(.*)', _str, re.MULTILINE)
                if len(_ret[0]) > 1:
                    _rawname = strip(_ret[0][0])
                    _name = strip(_ret[0][0]).replace('_', '').lower()
                    _id = strip(_ret[0][1])
                    proto_ids[_name + 'proto'] = {
                        'id': _id,
                        'name': _name,
                        "rawname" : _rawname,
                        'comment': _comment,
                    }
            context.proto_ids = proto_ids

        if message_desc.name in MissingProtoList:
            return int(MissingProtoList[message_desc.name])

        message_name = message_desc.name.lower()
        if message_name in context.proto_ids:
            id = context.proto_ids[message_name]['id']
            if id is not None:
                return int(id)
        else:
            print("[\"" + message_desc.name + "\"] = -1")
            return -1

        return -1

    def get_protocol_category(self, message_desc):
        message_name = message_desc.name

        if message_name.startswith('C2S'):
            return "Request"

        if message_name.startswith('S2C'):
            return "Response"

        return "Notification"