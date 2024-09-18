import cherrypy
import xml.etree.ElementTree as ET
import classes
import sqlalchemy
from sqlalchemy import select
import os

##cherrypy.tre.mountko

##css_dir = os.path.dirname(os.path.realpath(__file__)) + '/css'
##css_handler = cherrypy.tools.staticdir.handler(section="/css", dir=css_dir)
##cherrypy.tree.mount(css_handler, '/css')

class EntryPoint(object):
    @cherrypy.expose
    def index(self):
        return """
<html>
<head>
<title> Post your XML</title>
</head>
<body>
    <h1>Submit XML For Visualization And Editing</h1>
    <form method="POST" action="postXml">
        <textarea cols="80" rows="12" name="xml">
        </textarea>
        <button type="submit">Submit</button>
    </form>
</body>
</html>
        """
    @cherrypy.expose
    def postXml(self, xml):
        try:
            self.__parseXmlFromString(xml)
        except sqlalchemy.exc.IntegrityError:
            pass
        raise cherrypy.HTTPRedirect("/list")

    @cherrypy.expose
    def list(self):
        session = classes.Session()
        stmt = select(classes.Order)
        #iterate over the results to pull them from the db (greedy loading)
        orders = [_[0] for _ in session.execute(stmt)] 
        html = """
<html>
<head>
<title>Listing of Orders</title>
</head>
<body>
        """
        for order in orders:
            html += '<form id="blah" name="blah" method="POST" action="updateOrder">'
            html += '<input type="hidden" name="orderId" value="'+order.id+'" />'
            html += '<label>Reference Number</label><input name="referenceNum" value="'+order.referenceNum.num+'">'
            html += '<label>Country Code</label><input name="countryCode" value="'+order.countryCode.code+'">'
            html += '<div id="address">'
            html += '   <label>Full Name</label><input name="address.fullName" value="'+order.address.fullName+'">'
            html += '   <label>Address Type</label><input name="address.addressType" value="'+order.address.addressType+'">'
            html += '   <label>Line 1</label><input name="address.addressLine1" value="'+order.address.addressLine1+'">'
            html += '   <label>Line 2</label><input name="address.addressLine2" value="'+order.address.addressLine2+'">'
            html += '</div><!--address-->'
            html += '<div id="customer">'
            html += '   <label>Customer Code</label><input name="customer.customerCode" value="'+order.customer.customerCode+'">'
            html += '   <label>First Name</label><input name="customer.firstName" value="'+order.customer.firstName+'">'
            html += '   <label>Last Name</label><input name="customer.lastName" value="'+order.customer.lastName+'">'
            html += '   <label>Phone</label><input name="customer.phone" value="'+order.customer.phone+'">'
            html += '   <label>Email</label><input name="customer.email" value="'+order.customer.email+'">'
            html += '</div><!--customer-->'
            html += '<div id="order_lines">'
            for line in order.orderLines.orderLines:
                html += '   <div id="order_line">'
                html += '       <input type="hidden" name="orderLine.id" value="'+line.id+'" />'
                html += '       <label>Item Number</label><input name="orderLine.itemNum" value="'+line.itemNum+'">'
                html += '       <label>Item Description</label><input name="orderLine.itemDescription" value="'+line.itemDescription+'">'
                html += '   </div><!--order_line-->'
            html += '</div><!--order_lines-->'
            html += '<input type="submit" />'
            html += "</form>"
        html += '</body></html>'
        return html

    @cherrypy.expose
    def updateOrder(self, *args, **kwargs):
        session = classes.Session()
        params = cherrypy.request.params
        orderId = params['orderId']
        stmt = select(classes.Order).where(classes.Order.id == orderId)
        order = [_[0] for _ in session.execute(stmt)].pop()
        order.referenceNum.num=params['referenceNum']
        order.countryCode.code=params['countryCode']
        order.address.fullName=params['address.fullName']
        order.address.addressType=params['address.addressType']
        order.address.addressLine1=params['address.addressLine1']
        order.address.addressLine2=params['address.addressLine2']
        order.customer.customerCode=params['customer.customerCode']
        order.customer.firstName=params['customer.firstName']
        order.customer.lastName=params['customer.lastName']
        order.customer.phone=params['customer.phone']
        order.customer.email=params['customer.email']
        for i,v in enumerate(params['orderLine.id']):
            id = v
            orderLine = [_ for _ in order.orderLines.orderLines if _.id == id].pop()
            orderLine.itemNum = params['orderLine.itemNum'][i]
            orderLine.itemDescription = params['orderLine.itemDescription'][i]

        session.add(order)
        session.commit()
        raise cherrypy.HTTPRedirect("/list")


    def __parseXmlFromString(self, xml):
        orders = classes.Order.consumeEnvelopeForListOfOrder(xml)
        session = classes.Session()
        for o in orders:
            session.add(o)
        session.commit()
        return


if __name__ == '__main__':
    classes.Base.metadata.create_all(classes.engine)
    cherrypy.quickstart(EntryPoint())
