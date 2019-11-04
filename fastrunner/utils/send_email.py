#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/10/22 15:48
# @Author  : liwaiqiang
# @Site    : 发送邮件的方法
# @File    : send_email.py
# @Software: PyCharm
import io
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from fastrunner.utils import response
from FasterRunner.settings import EMAIL_SEND_USERNAME, EMAIL_SEND_PASSWORD ,SMPT_SERVER


def send_email_reports(email_setting,summary):

    if '@sina.com' in EMAIL_SEND_USERNAME:
        smtp_server = 'smtp.sina.com'
    elif '@163.com' in EMAIL_SEND_USERNAME:
        smtp_server = 'smtp.163.com'
    elif '@qq.com' in EMAIL_SEND_USERNAME:
        smtp_server = 'smtp.exmail.qq.com'
    else:
        smtp_server = SMPT_SERVER


    successes = 0
    total = 0
    failures = 0
    rate = 0
    try:
        for item in summary['details']:
            total = total + 1
            if item['success'] == True:
                successes = successes + 1
            else:
                failures = failures + 1
        if total != 0:
            rate = ( successes / total ) * 100
            rate = round(rate,2)
    except BaseException:
        return response.EMAIL_STRATEGY_ERROR


    strategy = email_setting['strategy']
    threshold = float(email_setting['threshold'])
    # 只有当邮件策略为 1-始终发送 4-成功率低于阈值发送
    if "1"== strategy or ("4" == strategy and rate < threshold ):
        subject = "接口测试：" +"通过率-" + str(rate) + "% -" + email_setting["taskname"]
        receiver = email_setting['receiver']
        body_text = email_context(summary)
        body = MIMEText(body_text, _subtype='html', _charset='gb2312')

        msg = MIMEMultipart('related')
        msg['Subject'] = subject
        msg['from'] = EMAIL_SEND_USERNAME
        msg['to'] = receiver
        msg.attach(body)
        try:
            smtp = smtplib.SMTP()
            smtp.connect(smtp_server)
            smtp.login(EMAIL_SEND_USERNAME, EMAIL_SEND_PASSWORD)
            smtp.sendmail(EMAIL_SEND_USERNAME, receiver.split(';'), msg.as_string())
            smtp.quit()
        except BaseException:
            return response.EMAIL_SEND_ERROR
        return response.EMAIL_SEND_SUCCESS

def email_context(summary):
    successes = 0
    total = 0
    failures = 0
    rate = 0

    # 将用例情况罗列出来
    details_text =""
    for item in summary['details']:
        total = total + 1
        if item['success'] == True:
            successes = successes + 1
            details_text = details_text + """
                <tr>  
                        <td colspan="2">""" + item['name'] + """</td>  
                        <td colspan="2"><b><span style="color:#66CC00">PASS</span></b></td>   
                    </tr>  
                <tr>
                """
        else:
            failures = failures + 1
            details_text = details_text + """
                <tr>  
                        <td colspan="2">""" + item['name'] + """</td>  
                        <td colspan="2"><b><span style="color:#FF3333">FAIL</span></b></td> 
                    </tr>  
                <tr>
                """
    if total != 0:
        rate = ( successes / total ) * 100
        rate = round(rate, 2)
    mail_body = """
    <div style="width:100%;float:left"> 
    	<table cellspacing="0" cellpadding="4" border="1" align="left">  
    		<thead>
    			<tr bgcolor="#F3F3F3">
    				<td style="text-align:center" colspan="4"><b>接口测试报告</b></td>    
    			</tr>                           
    			<tr bgcolor="#F3F3F3">
    				<td><b>总用例数</b></td>
    				<td><b>通过数</b></td>
    				<td style="width:60px"><b>失败数</b></td>
    				<td style="width:100px"><b>通过率</b></td>
    			</tr>
    			<!----------------------------此处放置总体测试统计数据------------------------------->
    			<tr>
    				<td>""" + str(total) + """</td>
    				<td><b><span style="color:#66CC00">""" + str(successes) + """</span></b></td>
    				<td><b><span style="color:#FF3333">""" + str(failures) + """</span></b></td>
    				<td>""" + str(rate) + """%</td>
    			</tr>
    			<tr bgcolor="#F3F3F3">  
    				<td colspan="2"><b>用例名称</b></td>  
    				<td colspan="2"><b>状态</b></td>
    			</tr>  
    		</thead>  
    		<tbody>
    		<!----------------------------此处放置测试用例执行详情------------------------------->
            """ + details_text + """
    		</tbody>
    	</table>
    </div>
    """
    return mail_body

