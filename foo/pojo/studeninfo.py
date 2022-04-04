class StudentInfo:
    """
    用户名
    性别
    部门
    身份
    卡号
    帐号
    余额
    有效期
    状态
    证件号码
    卡片类型
    证件类型
    """
    def __init__(self, name, sex, partment, identity, userId, cardNum, cardId, money,
                 date, status, certCode, cardType, certType):
        self.cardNum = cardNum
        self.userId = userId
        self.identity = identity
        self.partment = partment
        self.sex = sex
        self.name = name
        self.cardId = cardId
        self.money = money
        self.date = date
        self.status = status
        self.certCode = certCode
        self.cardType = cardType
        self.certType = certType

    def __init__(self, doc):
        self.name = self.find_text(doc, "#lblInName")
        self.sex = self.find_text(doc, "#lblInSex")
        self.partment = self.find_text(doc, "#lblInDep")
        self.identity = self.find_text(doc, "#lblClsName0")
        self.userId = self.find_text(doc, "#lblInPercode")
        self.cardNum = self.find_text(doc, "#lblCardNum0")
        self.cardId = self.find_text(doc, "#lblInAcc")
        self.money = self.find_text(doc, "#lblOne0")
        self.date = self.find_text(doc, "#lblLostDate0")
        self.status = self.find_text(doc, "#lblAccStatus0")
        self.certCode = self.find_text(doc, "#lblCertCode0")
        self.cardType = self.find_text(doc, "#lblAccType0")
        self.certType = self.find_text(doc, "#lblCertTypeNum0")

    def find_text(self, doc, name):
        return doc.find(name).text()