#-*-coding: utf-8 -*-
import os, json, logging
from collections import defaultdict
from PyQt5.QtCore import QObject
from PyQt5.QAxContainer import QAxWidget

class KiwoomAPI(QObject):
    """
        Layer Class connecting python controller to the Kiwoom OpenAPI ocx module.
    """
    ERROR_MESSAGES = {
        "0": "정상처리",
        "-1": "미접속상태",
        "-100": "로그인시 접속 실패(아이피오류 또는 접속정보 오류)",
        "-101": "서버 접속 실패",
        "-102": "버전처리가 실패하였습니다.",
        "-103": "TrCode가 존재하지 않습니다.",
        "-104": "해외 OpenAPI 미신청",
        "-200": "조회 과부하",
        "-201": "주문 과부하",
        "-202": "조회 입력값(명칭/누락) 오류",
        "-300": "주문 입력값 오류",
        "-301": "계좌비밀번호를 입력하십시오.",
        "-302": "타인계좌는 사용할 수 없습니다.",
        "-303": "경고 - 주문수량 200개 초과",
        "-304": "제한 - 주문수량 400개 초과"
    }

    __events = dict(
        OnReceiveTrData=defaultdict(list),
        OnReceiveRealData={
            "해외옵션호가" : [],
            "해외옵션시세" : [],
            "해외선물호가" : [],
            "해외선물시세" : [],
        },
        OnReceiveMsg=[],
        OnReceiveChejanData=[],
        OnEventConnect=[]
    )

    def __init__(self):
        super().__init__()
        self.ocx = QAxWidget("KFOPENAPI.KFOpenAPICtrl.1")
        self.__event_connector(KiwoomAPI.__events)
        self.event = KiwoomAPI.__events

    def __event_connector(self, events):
        for event in events.keys():
            getattr(self.ocx, event).connect(self.trigger(event))

    @staticmethod
    def on(event, screen=None, realType=None):
        """ Register event handlers """
        def decorator(func):
            if event == 'OnReceiveTrData':
                KiwoomAPI.__events[event][screen].append(func)
            elif event == 'OnReceiveRealData':
                if realType not in KiwoomAPI.__events[event]:
                    raise ValueError("Unknown realtype <%s> is registered"%realType)
                KiwoomAPI.__events[event][realType].append(func)
            else:
                KiwoomAPI.__events[event].append(func)
        return decorator

    def trigger(self, event):
        """ Call appropriate event handlers when event comes from the server """

        def triggered(*args):
            if event == "OnReceiveTrData":
                eventhandlers = KiwoomAPI.__events[event][args[0]]
            elif event == "OnReceiveRealData":
                eventhandlers = KiwoomAPI.__events[event][args[1]]
            else:
                eventhandlers = KiwoomAPI.__events[event]

            for func in eventhandlers:
                func(self, *args)
        return triggered


    """
        Methods defined bellow are automatically generated by 
        API_function_generator.py via kiwoomAPI.json in which 
        API function prototypes and descriptions are described.
        these files are located in root/utils directory.
    """
    def GetAPIModulePath(self, *args):
        """OpenAPI모듈의 경로를 반환한다."""
        return self.ocx.dynamicCall("GetAPIModulePath()", *args)

    def SendOrder(self, *args):
        """주문을 서버로 송신한다."""
        return self.ocx.dynamicCall("SendOrder(str, str, str, int, str, int, str, str, str, str)", *args)

    def GetGlobalOptionItemlist(self, *args):
        """해외선물 상품리스트를 반환한다."""
        return self.ocx.dynamicCall("GetGlobalOptionItemlist()", *args)

    def GetConnectState(self, *args):
        """현재 접속상태를 반환한다."""
        return self.ocx.dynamicCall("GetConnectState()", *args)

    def GetGlobalFutOpCodeInfoByCode(self, *args):
        """해외선물옵션 종목코드정보를 종목코드별로 반환한다."""
        return self.ocx.dynamicCall("GetGlobalFutOpCodeInfoByCode(str)", *args)

    def CommConnect(self, *args):
        """로그인 윈도우를 실행한다."""
        return self.ocx.dynamicCall("CommConnect(int)", *args)

    def GetGlobalOptionMonthByItem(self, *args):
        """해외옵션 월물리스트를 상품별로 반환한다."""
        return self.ocx.dynamicCall("GetGlobalOptionMonthByItem(str)", *args)

    def GetGlobalOptionActPriceByItem(self, *args):
        """해외옵션행사가리스트를 상품별로 반환한다."""
        return self.ocx.dynamicCall("GetGlobalOptionActPriceByItem()", *args)

    def GetRepeatCnt(self, *args):
        """수신데이타(반복횟수)를 반환한다."""
        return self.ocx.dynamicCall("GetRepeatCnt(str, str)", *args)

    def GetGlobalFutureCodelist(self, *args):
        """해외상품별 해외선물 종목코드 리스트를 반환한다."""
        return self.ocx.dynamicCall("GetGlobalFutureCodelist(str)", *args)

    def GetGlobalFutureItemTypelist(self, *args):
        """해외선물 상품타입리스트를 반환한다."""
        return self.ocx.dynamicCall("GetGlobalFutureItemTypelist()", *args)

    def GetGlobalFutOpCodeInfoByType(self, *args):
        """해외선물옵션 종목코드 정보를 타입별로 반환한다."""
        return self.ocx.dynamicCall("GetGlobalFutOpCodeInfoByType(int, str)", *args)

    def GetCommFullData(self, trCode, rqName, gubun):
        """수신된 전체데이터를 반환한다."""
        return self.ocx.dynamicCall("GetCommFullData(str, str, int)", trCode, rqName, gubun)

    def CommTerminate(self):
        """OpenAPI의 서버 접속을 해제한다."""
        self.ocx.dynamicCall("CommTerminate()")

    def GetGlobalFutureItemlistByType(self, *args):
        """해외선물 상품리스트를 타입별로 반환한다."""
        return self.ocx.dynamicCall("GetGlobalFutureItemlistByType(str)", *args)

    def SetInputValue(self, field, value):
        """조회 입력값을 셋팅한다"""
        self.ocx.dynamicCall("SetInputValue(str, str)", field, value)

    def GetConvertPrice(self, *args):
        """가격 진법에 따라 변환된 가격을 반환한다."""
        return self.ocx.dynamicCall("GetConvertPrice(str, str, int)", *args)

    def CommRqData(self, rqName, trCode, prev, scrNo):
        """조회를 서버로 송신한다"""
        return self.ocx.dynamicCall("CommRqData(str,str,str,str)", rqName, trCode, prev, scrNo)

    def GetGlobalFutureCodeByItemMonth(self, *args):
        """해외선물종목코드를 상품/월물별로 반환한다."""
        return self.ocx.dynamicCall("GetGlobalFutureCodeByItemMonth(str, str)", *args)

    def GetGlobalOptionCodeByMonth(self, *args):
        """해외옵션 종목코드를 상품/콜풋/행사가/월물별로 반환한다."""
        return self.ocx.dynamicCall("GetGlobalOptionCodeByMonth(str,str,str,str)", *args)

    def GetGlobalFutureItemlist(self, *args):
        """해외선물 상품리스트를 반환한다."""
        return self.ocx.dynamicCall("GetGlobalFutureItemlist()", *args)

    def GetCommData(self, trCode, rqName, index, fieldName):
        """수신데이타를 반환한다."""
        return self.ocx.dynamicCall("GetCommData(str, str, int, str)", trCode, rqName, index, fieldName)

    def DisconnectRealData(self, *args):
        """화면 내의 모든 리얼데이터 요청을 제거한다."""
        self.ocx.dynamicCall("DisconnectRealData(str)", *args)

    def GetGlobalOptionCodelist(self, *args):
        """해외상품별 해외옵션 종목코드 리스트를 반환"""
        return self.ocx.dynamicCall("GetGlobalFutureCodelist(str)", *args)

    def GetLoginInfo(self, *args):
        """로그인 사용자 정보를 반환한다."""
        return self.ocx.dynamicCall("GetLoginInfo(str)", *args)

    def GetChjanData(self, *args):
        """체결잔고 실시간 데이타를 반환한다."""
        return self.ocx.dynamicCall("GetChejanData(int)", *args)

    def GetCommRealData(self, realType, nFid):
        """실시간데이타를 반환한다.
           realType에 아무거나 입력해도 동일한 결과 반환
        """
        return self.ocx.dynamicCall("GetCommRealData(str,int)", realType, nFid)
        